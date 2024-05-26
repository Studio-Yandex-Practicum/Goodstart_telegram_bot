from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CommandHandler, ContextTypes

from schooling.models import Teacher, Student
from bot.utils import check_user_from_db
from bot.messages_texts.constants import (
    WELCOME_MSG, REGISTRATION_MSG,
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    `/start` command handler.

    If the user is registered in the database, sends a welcome message,
    else sends a registration link.
    """
    telegram_id = update.effective_chat.id
    user = await check_user_from_db(telegram_id, (Teacher, Student))

    registration_buttons = ReplyKeyboardMarkup(
        [['/registration']],
        resize_keyboard=True,
    )

    if user:
        await context.bot.send_message(
            chat_id=telegram_id,
            text=WELCOME_MSG,
        )
    else:
        await context.bot.send_message(
            chat_id=telegram_id,
            text=REGISTRATION_MSG,
            reply_markup=registration_buttons,
        )

start_handler = CommandHandler(start.__name__, start)
