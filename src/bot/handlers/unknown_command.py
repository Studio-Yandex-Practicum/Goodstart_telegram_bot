from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters

from core.logging import log_errors
from bot.handlers.help import help


@log_errors
async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Echo messages handler."""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Неизвестная команда, выберите что-то из того, что я умею!',
    )
    await help(update, context)

unknown_command_handler = MessageHandler(filters.TEXT & (~filters.COMMAND),
                                         unknown)
