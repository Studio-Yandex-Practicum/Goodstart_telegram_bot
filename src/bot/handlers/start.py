from telegram import Update
from telegram.ext import CommandHandler, ContextTypes


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/start command handler."""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=(
            'Привет, я бот онлайн школы GoodStart.\n\n'
            'Здесь ты найдёшь лучших преподавателей.'
        ),
    )

start_handler = CommandHandler('start', start)
