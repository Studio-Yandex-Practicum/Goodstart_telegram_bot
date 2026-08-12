# Разместить как schooling/services/trial_lesson_broadcast.py
# (создайте папку services/ с пустым __init__.py, если её ещё нет)
#
# Здесь — общая логика рассылки. Её использует и management-команда
# (для запуска из консоли), и кнопка в админке (для запуска руками).

import asyncio
import logging

from django.conf import settings
from telegram import Bot
from telegram.error import BadRequest, Forbidden
from telegram.request import HTTPXRequest

from bot.keyboards import get_trial_lesson_markup
from schooling.models import Student, TrialLessonRequest

logger = logging.getLogger(__name__)

DEFAULT_TEXT = (
    'Привет! 👋 Хотите попробовать бесплатный пробный урок?\n'
    'Нажмите на кнопку ниже, чтобы записаться — '
    'наш менеджер свяжется с вами для подтверждения времени.'
)


def send_trial_lesson_broadcast(telegram_ids=None, text=None):
    """
    Синхронная обёртка для запуска рассылки из обычного (не async) кода:
    из management-команды или из view в Django admin.

    :param telegram_ids: список telegram_id; если не передан — берутся
        все студенты из Student.
    :param text: текст сообщения; если не передан — используется текст
        по умолчанию.
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

    sent, failed = asyncio.run(
        _send_messages(telegram_ids, text or DEFAULT_TEXT),
    )
    return sent, failed, skipped


async def _send_messages(telegram_ids, text):
    """Асинхронно рассылает сообщения по списку telegram_id."""
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
    async with bot:
        for telegram_id in telegram_ids:
            try:
                await bot.send_message(
                    chat_id=telegram_id,
                    text=text,
                    reply_markup=markup,
                )
                sent += 1
            except Forbidden:
                logger.warning(
                    f'{telegram_id}: пользователь заблокировал бота',
                )
                failed += 1
            except BadRequest as e:
                logger.warning(f'{telegram_id}: чат не найден ({e})')
                failed += 1
            except Exception as e:
                logger.error(f'{telegram_id}: ошибка отправки — {e}')
                failed += 1

    return sent, failed
