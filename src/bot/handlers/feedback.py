from telegram import Update
from telegram.ext import (
    CommandHandler, CallbackContext, ConversationHandler, filters,
    MessageHandler,
)

from core.logging import log_errors
from schooling.models import Teacher, Student
from bot.utils import check_user_from_db
from bot.states import UserStates

THEME, BODY = range(2)


@log_errors
async def feedback(
    update: Update,
    context: CallbackContext,
):
    """
    `/feedback` command handler.

    Add description.
    """
    telegram_id = update.effective_chat.id
    user = await check_user_from_db(telegram_id, (Teacher, Student))

    if user:
        await update.message.reply_text(
            'Пожалуйста, напишите тему обращения:'
        )
        return UserStates.FEEDBACK_SUBJECT_MSG
    else:
        await update.message.reply_text(
            'У вас нет доступа к этой команде.'
        )
        return ConversationHandler.END


async def subject(update: Update, context: CallbackContext) -> int:
    context.user_data['subject'] = update.message.text
    await update.message.reply_text(
        'Теперь напишите тело обращения:'
    )
    return UserStates.FEEDBACK_BODY_MSG


async def body(update: Update, context: CallbackContext) -> int:
    context.user_data['body'] = update.message.text

    subject = context.user_data['subject']
    body = context.user_data['body']

    print(subject)
    print(body)

    await update.message.reply_text(
        'Спасибо за ваше обращение!'
    )
    return ConversationHandler.END


@log_errors
async def cancel(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text('Обращение отменено.')
    return ConversationHandler.END


feedback_handler = ConversationHandler(
    entry_points=[CommandHandler(feedback.__name__, feedback)],
    states={
        UserStates.FEEDBACK_SUBJECT_MSG: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                subject
            )
        ],
        UserStates.FEEDBACK_BODY_MSG: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                body
            )
        ],
    },
    fallbacks=[CommandHandler('cancel', cancel)],
)
