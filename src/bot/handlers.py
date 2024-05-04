from telegram import Update
from telegram.ext import filters, ContextTypes, CommandHandler, MessageHandler

from core.logging import log_errors


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for the /start command."""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=(
            'Привет, я бот онлайн школы GoodStart.\n\n'
            'Здесь ты найдёшь лучших преподавателей.'
        ),
    )


@log_errors
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for echoing user messages."""
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=update.message.text
    )


start_handler = CommandHandler('start', start)
echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
