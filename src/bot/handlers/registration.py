from telegram import KeyboardButton, ReplyKeyboardMarkup, Update, WebAppInfo
from telegram.ext import ContextTypes, CommandHandler
from django.urls import reverse
from django.conf import settings

from core.logging import log_errors
from bot.messages_texts.constants import (
    REGISTRATION_HELP_TEXT
)


@log_errors
async def user_consent_to_registration(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
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
                        )
                    )
                )
            ]],
            resize_keyboard=True
        ),
    )


@log_errors
async def user_refuses_to_registration(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    """
    `/refuses` command handler.

    Add description.
    """
    telegram_id = update.effective_chat.id
    await context.bot.send_message(
        chat_id=telegram_id,
        text='Test message refuses',
    )


registration_handler = CommandHandler(
    'registration', user_consent_to_registration
)
refuses_registration_handler = CommandHandler(
    'refuses', user_refuses_to_registration
)
