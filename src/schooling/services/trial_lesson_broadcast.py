# Разместить как schooling/services/trial_lesson_broadcast.py
# (создайте папку services/ с пустым __init__.py, если её ещё нет)
#
# Здесь — общая логика рассылки. Её использует и management-команда
# (для запуска из консоли), и кнопка в админке (для запуска руками).
#
# Защита от блокировки бота Telegram при массовой рассылке:
#   - сообщения отправляются не параллельно, а последовательно с паузой
#     (MESSAGES_PER_SECOND), т.к. у Telegram Bot API есть общий лимит
#     ~30 сообщений в секунду на бота, и близкая к лимиту скорость
#     повышает риск временной блокировки (429 Too Many Requests);
#   - если Telegram всё же ответил 429 (RetryAfter), ждём именно
#     столько, сколько он просит, и повторяем попытку для этого же
#     получателя (с ограничением по числу попыток).

import asyncio
import logging

from django.conf import settings
from telegram import Bot
from telegram.error import BadRequest, Forbidden, RetryAfter, TimedOut
from telegram.request import HTTPXRequest

from bot.keyboards import get_trial_lesson_markup
from schooling.models import Student, TrialLessonBroadcastMessage, TrialLessonRequest
from schooling.services.telegram_markdown import markdown_to_telegram_markdown_v2

logger = logging.getLogger(__name__)

# Сколько сообщений в секунду отправляем. У Telegram лимит около 30/сек
# на бота суммарно по всем чатам — берём с запасом, чтобы не приближаться
# к границе и не подставлять бота под блокировку/ограничение.
MESSAGES_PER_SECOND = 20
DELAY_BETWEEN_MESSAGES = 1 / MESSAGES_PER_SECOND

# Сколько раз повторяем отправку одному получателю, если Telegram
# ответил "подожди" (RetryAfter) или временной ошибкой сети.
MAX_RETRIES = 3


class BroadcastTextError(Exception):
    """
    Telegram отклонил сам текст сообщения (ошибка разметки MarkdownV2).
    Это не зависит от получателя — при такой ошибке нет смысла
    продолжать рассылку остальным, все попытки будут падать так же.
    """


def send_trial_lesson_broadcast(telegram_ids=None, text=None):
    """
    Синхронная обёртка для запуска рассылки из обычного (не async) кода:
    из management-команды или из view в Django admin.

    :param telegram_ids: список telegram_id; если не передан — берутся
        все студенты из Student.
    :param text: текст сообщения в Markdown (**жирный**, *курсив*,
        [текст](ссылка)); если не передан — берётся текст, сохранённый
        в админке (TrialLessonBroadcastMessage). Перед отправкой
        конвертируется в Telegram MarkdownV2.
    :return: кортеж (sent, failed, skipped) — количество успешных,
        неуспешных отправок и пропущенных (у кого уже есть заявка
        в статусе NEW).
    """
    if telegram_ids is None:
        telegram_ids = list(
            Student.objects.values_list('telegram_id', flat=True),
        )

    # Пропускаем тех, у кого уже есть необработанная (NEW) заявка —
    # незачем звать их ещё раз, пока менеджер не разобрался с текущей.
    already_requested = set(
        TrialLessonRequest.objects.filter(
            status=TrialLessonRequest.NEW,
            telegram_id__in=telegram_ids,
        ).values_list('telegram_id', flat=True),
    )
    skipped = len(already_requested)
    telegram_ids = [
        tg_id for tg_id in telegram_ids if tg_id not in already_requested
    ]

    if not telegram_ids:
        return 0, 0, skipped

    if text is None:
        text = TrialLessonBroadcastMessage.load().text
    telegram_text = markdown_to_telegram_markdown_v2(text)

    sent, failed = asyncio.run(
        _send_messages(telegram_ids, telegram_text),
    )
    return sent, failed, skipped


async def _send_messages(telegram_ids, text):
    """Асинхронно и с ограничением скорости рассылает сообщения."""
    request = HTTPXRequest(
        connection_pool_size=20,
        connect_timeout=30,
        read_timeout=30,
    )
    # Тот же кастомный base_url, что используется в bot_interface.py
    bot = Bot(
        token=settings.TELEGRAM_TOKEN,
        base_url='http://195.133.8.27/bot',
        request=request,
    )
    markup = get_trial_lesson_markup()

    sent, failed = 0, 0
    total = len(telegram_ids)

    async with bot:
        for i, telegram_id in enumerate(telegram_ids, start=1):
            try:
                success = await _send_one(bot, telegram_id, text, markup)
            except BroadcastTextError as e:
                # Текст сообщения не прошёл разметку — дальше слать
                # нечего, все оставшиеся получатели считаются неудачей.
                logger.error(
                    f'{e} Рассылка прервана, отправлено {i - 1}/{total}, '
                    f'остальные {total - i + 1} помечены как неудача. '
                    'Проверьте текст рассылки в админке.',
                )
                failed += total - i + 1
                break

            if success:
                sent += 1
            else:
                failed += 1

            # Пауза после каждого сообщения, кроме последнего —
            # держим темп ниже общего лимита Telegram.
            if i < total:
                await asyncio.sleep(DELAY_BETWEEN_MESSAGES)

            if i % 100 == 0:
                logger.info(f'Рассылка: отправлено {i}/{total}')

    return sent, failed


async def _send_one(bot, telegram_id, text, markup):
    """
    Отправляет одно сообщение с повторными попытками при 429/таймаутах.
    Возвращает True при успехе, False — если получатель недостижим
    (заблокировал бота, чат не найден) или попытки исчерпаны.
    """
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            await bot.send_message(
                chat_id=telegram_id,
                text=text,
                parse_mode='MarkdownV2',
                reply_markup=markup,
            )
            return True

        except Forbidden:
            # Пользователь заблокировал бота — повторять бессмысленно.
            logger.warning(
                f'{telegram_id}: пользователь заблокировал бота',
            )
            return False

        except BadRequest as e:
            # Ошибка разметки в самом тексте (не экранированный спецсимвол
            # и т.п.) — одинаково провалится для всех получателей,
            # продолжать рассылку с этим текстом бессмысленно.
            if 'parse entities' in str(e).lower():
                raise BroadcastTextError(
                    f'Telegram отклонил текст рассылки: {e}',
                ) from e

            # Некорректный chat_id / чат не найден — повторять бессмысленно.
            logger.warning(f'{telegram_id}: чат не найден ({e})')
            return False

        except RetryAfter as e:
            # Telegram сам просит подождать — ждём ровно столько,
            # сколько он указал, и пробуем этого же получателя ещё раз.
            wait_seconds = e.retry_after + 1
            logger.warning(
                f'{telegram_id}: Telegram просит подождать '
                f'{wait_seconds} сек. (попытка {attempt}/{MAX_RETRIES})',
            )
            await asyncio.sleep(wait_seconds)

        except TimedOut:
            logger.warning(
                f'{telegram_id}: таймаут сети, повтор '
                f'(попытка {attempt}/{MAX_RETRIES})',
            )
            await asyncio.sleep(2)

        except Exception as e:
            logger.error(f'{telegram_id}: ошибка отправки — {e}')
            return False

    logger.error(
        f'{telegram_id}: не удалось отправить после {MAX_RETRIES} попыток',
    )
    return False