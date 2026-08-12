from asgiref.sync import sync_to_async
from loguru import logger
from telegram import Update
from telegram.ext import CallbackQueryHandler, ContextTypes

from bot.keyboards import TRIAL_LESSON_CALLBACK_DATA
from schooling.models import TrialLessonRequest


async def trial_lesson_signup(
    update: Update, context: ContextTypes.DEFAULT_TYPE,
):
    """Обрабатывает нажатие кнопки 'Записаться на пробный урок'."""
    query = update.callback_query
    await query.answer()

    user = query.from_user
    full_name = f'{user.first_name or ""} {user.last_name or ""}'.strip()

    # Не создаём дубль, если уже есть необработанная заявка от этого юзера
    request, created = await sync_to_async(
        TrialLessonRequest.objects.get_or_create,
    )(
        telegram_id=user.id,
        status=TrialLessonRequest.NEW,
        defaults={
            'username': user.username,
            'full_name': full_name,
        },
    )

    if created:
        logger.info(f'Создана заявка на пробный урок от {user.id}')
        # Убираем кнопку, чтобы нельзя было нажать повторно
        try:
            await query.edit_message_reply_markup(reply_markup=None)
        except Exception:
            pass
        await query.message.reply_text(
            'Спасибо! Ваша заявка на пробный урок принята 🎉\n'
            'Наш менеджер свяжется с вами в ближайшее время.',
        )
    else:
        await query.message.reply_text(
            'Вы уже записались на пробный урок. Мы скоро с вами свяжемся!',
        )


# Регистрируется как отдельный top-level handler (не входит в состояния
# ConversationHandler), т.к. кнопка может прийти пользователю, который
# ещё не начинал диалог с ботом (/start не нажат).
trial_lesson_handler = CallbackQueryHandler(
    trial_lesson_signup,
    pattern=f'^{TRIAL_LESSON_CALLBACK_DATA}$',
)

# В bot_interface.py, в _build_app(), нужно:
# 1) добавить импорт:
#    from bot.handlers.trial_lesson import trial_lesson_handler
# 2) добавить в список app.add_handlers([...]) сам trial_lesson_handler,
#    например перед main_handler, чтобы он ловил колбэк независимо от
#    состояния диалога:
#
#    app.add_handlers([
#        trial_lesson_handler,
#        main_handler,
#        start_handler,
#        help_handler,
#        ...
#    ])
