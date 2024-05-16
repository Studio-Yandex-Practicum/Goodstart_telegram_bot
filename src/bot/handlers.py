from telegram import Update
from telegram.ext import CommandHandler, ContextTypes, MessageHandler, filters

from core.logging import log_errors

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/start command handler."""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=(
            'Привет, я бот онлайн школы GoodStart.\n\n'
            'Здесь ты найдёшь лучших преподавателей.'
        ),
    )


@log_errors
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Echo messages handler."""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=update.message.text,
    )


start_handler = CommandHandler('start', start)
echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
