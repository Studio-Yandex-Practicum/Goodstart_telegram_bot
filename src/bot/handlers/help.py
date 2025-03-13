from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from bot.utils import check_user_from_db
from bot.messages_texts.constants import (
    UNKNOWN_USER_HELP_MSG, TEACHER_HELP_MSG, STUDENT_HELP_MSG,
)
from core.logging import log_errors
from django.conf import settings
from schooling.models import Teacher, Student
from schooling.signals_bot import send_message_to_user


@log_errors
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    `/help` command handler.

    Add description.
    """
    telegram_id = update.effective_chat.id
    user = await check_user_from_db(telegram_id, (Teacher, Student))

    if user.__class__.__name__ == 'Student':
        await send_message_to_user(
            bot_token=settings.TELEGRAM_TOKEN,
            user_id=telegram_id,
            message_text=STUDENT_HELP_MSG,
        )
    elif user.__class__.__name__ == 'Teacher':
        await send_message_to_user(
            bot_token=settings.TELEGRAM_TOKEN,
            user_id=telegram_id,
            message_text=TEACHER_HELP_MSG,
        )
    else:
        await context.bot.send_message(
            chat_id=telegram_id,
            text=UNKNOWN_USER_HELP_MSG,
        )

help_handler = CommandHandler(help.__name__, help)
