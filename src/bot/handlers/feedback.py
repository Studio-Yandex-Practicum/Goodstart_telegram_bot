# TODO: Должна быть доступна после регистрации и ученику и учителю
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import (
    CommandHandler, CallbackContext, ConversationHandler,
)

from core.logging import log_errors
from core.utils import send_feedback_email
from schooling.models import Teacher, Student
from bot.utils import check_user_from_db
from bot.states import UserStates
from bot.messages_texts.constants import (
    FEEDBACK_SUBJECT_REQUEST_MSG, FEEDBACK_SUBJECT_REQUEST_MSG_ERROR,
    FEEDBACK_BODY_REQUEST_MSG, FEEDBACK_SUCCESS_MSG,
    FEEDBACK_REMOVE_SUPPORT_KEYBOARD_MSG,
)


@log_errors
async def feedback(update: Update, context: CallbackContext):
    """
    `/feedback` command handler.

    Add description.
    """
    telegram_id = update.effective_chat.id
    user = await check_user_from_db(telegram_id, (Teacher, Student))

    if user:
        context.user_data['current_user'] = user
        await update.message.reply_text(
            text=FEEDBACK_REMOVE_SUPPORT_KEYBOARD_MSG,
            reply_markup=ReplyKeyboardRemove(),
        )
        await update.message.reply_text(FEEDBACK_SUBJECT_REQUEST_MSG)
        return UserStates.FEEDBACK_SUBJECT
    else:
        await update.message.reply_text(FEEDBACK_SUBJECT_REQUEST_MSG_ERROR)
        return ConversationHandler.END


async def subject(update: Update, context: CallbackContext):
    context.user_data['subject'] = update.message.text
    await update.message.reply_text(FEEDBACK_BODY_REQUEST_MSG)
    return UserStates.FEEDBACK_BODY


async def body(update: Update, context: CallbackContext):
    context.user_data['body'] = update.message.text

    subject = context.user_data['subject']
    body = context.user_data['body']
    user = context.user_data['current_user']

    await send_feedback_email(subject, body, user)

    await update.message.reply_text(FEEDBACK_SUCCESS_MSG)
    return UserStates.START

feedback_handler = CommandHandler(feedback.__name__, feedback)
