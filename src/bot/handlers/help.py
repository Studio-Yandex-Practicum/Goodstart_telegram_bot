from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from bot.utils import check_user_from_db
from bot.messages_texts.constants import (
    UNKNOWN_USER_HELP_MSG, TEACHER_HELP_MSG, STUDENT_HELP_MSG,
)
from core.logging import log_errors
from schooling.models import Teacher, Student


@log_errors
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    `/help` command handler.

    Add description.
    """
    telegram_id = update.effective_chat.id
    user = await check_user_from_db(telegram_id, (Teacher, Student))

    if not user:
        await context.bot.send_message(
            chat_id=telegram_id,
            text=UNKNOWN_USER_HELP_MSG,
        )
    elif user.__class__.__name__ == 'Teacher':
        await context.bot.send_message(
            chat_id=telegram_id,
            text=TEACHER_HELP_MSG,
        )
    else:
        await context.bot.send_message(
            chat_id=telegram_id,
            text=STUDENT_HELP_MSG,
        )

help_handler = CommandHandler(help.__name__, help)
