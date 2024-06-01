from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes, MessageHandler, filters

from bot.messages_texts.constants import REGISTRATION_SUCCESS_MSG


async def success_registration_webapp(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    """
    Выводит сообщение об успешной отправке данных из формы, убирает кнопку
    открытия webapp и удаляет сообщение с просьбой зарегистрироваться.

    """
    telegram_id = update.effective_chat.id
    registration_message_id = update.effective_message.message_id - 1
    await update.message.reply_html(
        text=REGISTRATION_SUCCESS_MSG,
        reply_markup=ReplyKeyboardRemove(),
    )
    await context.bot.delete_message(
        chat_id=telegram_id,
        message_id=registration_message_id,
    )

success_registration_webapp_handler = MessageHandler(
    filters.StatusUpdate.WEB_APP_DATA,
    success_registration_webapp,
)
