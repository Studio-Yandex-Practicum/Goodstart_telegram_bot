from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CommandHandler, ContextTypes

from schooling.models import Teacher, Student
from bot.utils import check_user_from_db


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """`/start` command handler."""
    telegram_id = update.effective_chat.id
    user = await check_user_from_db(
        telegram_id=telegram_id,
        from_models=(Teacher, Student),
    )

    if user:
        await context.bot.send_message(
            chat_id=telegram_id,
            text=(
                'Привет, я бот онлайн школы GoodStart.\n\n'
                'Здесь ты найдёшь лучших преподавателей.'
            ),
        )
    else:
        await context.bot.send_message(
            chat_id=telegram_id,
            text=(
                f'Привет, {update.effective_user.first_name}!\n\n'
                f'Похоже, ты еще не зарегистрирован в нашей онлайн школе '
                f'GoodStart.\nДавай зарегистрируемся прямо сейчас.'
            ),
            reply_markup=ReplyKeyboardMarkup(
                [['Начать регистрацию']],
                resize_keyboard=True,
            ),
        )

start_handler = CommandHandler('start', start)
