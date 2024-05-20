from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from django.urls import reverse
from django.conf import settings

from schooling.models import Teacher, Student
from bot.utils import check_user_from_db


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    `/start` command handler.

    If the user is registered in the database, sends a welcome message,
    else sends a registration link.
    """
    telegram_id = update.effective_chat.id
    user = await check_user_from_db(telegram_id, (Teacher, Student))

    welcome_msg = (
        'Привет, я бот онлайн школы GoodStart!\n\n'
        'Здесь ты найдёшь лучших преподавателей.'
    )
    registration_msg = (
        f'Привет, я бот онлайн школы GoodStart!\n\n'
        f'Похоже, ты еще не зарегистрирован в нашей онлайн школе '
        f'GoodStart.\nДавай зарегистрируемся прямо сейчас по ссылке '
        f'{settings.BASE_URL}{reverse("registration:registration")}'
    )

    await context.bot.send_message(
        chat_id=telegram_id,
        text=welcome_msg if user else registration_msg,
    )

start_handler = CommandHandler(start.__name__, start)
