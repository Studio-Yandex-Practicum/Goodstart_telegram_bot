from telegram import (
    ReplyKeyboardMarkup, Update, KeyboardButton, WebAppInfo,
)
from telegram.ext import CommandHandler, ContextTypes
from django.urls import reverse
from django.conf import settings

from core.logging import log_errors
from schooling.models import Teacher, Student
from bot.utils import check_user_from_db, check_user_application_exists
from bot.messages_texts.constants import (
    WELCOME_MSG, REGISTRATION_MSG, APPLICATION_EXISTS_MSG,
)
from bot.keyboards import get_root_markup
from bot.states import UserFlow


@log_errors
async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    """
    `/start` command handler.

    If the user is registered in the database, sends a welcome message,
    else sends a registration link.
    """
    telegram_id = update.effective_chat.id
    user = await check_user_from_db(telegram_id, (Teacher, Student))

    if user:
        user_flow = UserFlow(user)
        await user_flow.start()
        await context.bot.send_message(
            chat_id=telegram_id,
            text=WELCOME_MSG,
            reply_markup=await get_root_markup(),
        )
        return user_flow.state

    else:
        if await check_user_application_exists(telegram_id):
            await context.bot.send_message(
                chat_id=telegram_id,
                text=APPLICATION_EXISTS_MSG,
            )
        else:
            await update.message.reply_text(
                REGISTRATION_MSG,
                reply_markup=ReplyKeyboardMarkup.from_button(
                    KeyboardButton(
                        text='Открыть форму регистрации',
                        web_app=WebAppInfo(
                            url=(
                                f'{settings.BASE_URL}'
                                f'{
                                    reverse(
                                        'registration:registration',
                                        kwargs={'id': telegram_id},
                                    )
                                }'
                            ),
                        ),
                    ),
                    resize_keyboard=True,
                ),
            )

start_handler = CommandHandler(start.__name__, start,)
