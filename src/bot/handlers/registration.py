from telegram import KeyboardButton, ReplyKeyboardMarkup, Update, WebAppInfo
from telegram.ext import ContextTypes, CommandHandler
from django.urls import reverse
from django.conf import settings

from core.logging import log_errors
from bot.messages_texts.constants import REGISTRATION_HELP_TEXT


@log_errors
async def registration(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    """
    `/registration` command handler.

    Add description.
    """
    await update.message.reply_text(
        REGISTRATION_HELP_TEXT,
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[[
                KeyboardButton(
                    text='Открыть форму регистрации',
                    web_app=WebAppInfo(
                        url=(
                            f'{settings.BASE_URL}'
                            f'{reverse('registration:registration')}'
                        ),
                    ),
                ),
            ]],
            resize_keyboard=True,
        ),
    )

registration_handler = CommandHandler(
    registration.__name__, registration,
)
