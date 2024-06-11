from telegram import (
    Update, InlineKeyboardMarkup, KeyboardButton, WebAppInfo,
)
from telegram.ext import CommandHandler, ContextTypes
from django.urls import reverse
from django.conf import settings

from core.logging import log_errors
from schooling.models import Teacher, Student
from bot.utils import check_user_from_db
from bot.states import UserStates
from bot.messages_texts.constants import (
    UNKNOWN_USER_HELP_MSG,
)


@log_errors
async def schedule(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    `/schedule` command handler.

    Add description.
    """
    telegram_id = update.effective_chat.id
    user = await check_user_from_db(telegram_id, (Teacher, Student))
    if not user:
        await context.bot.send_message(
            chat_id=telegram_id,
            text=UNKNOWN_USER_HELP_MSG,
        )
    else:
        await update.message.reply_text(
            'Посмотреть расписание',
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[
                    KeyboardButton(
                        text='Посмотреть расписание',
                        web_app=WebAppInfo(
                            url=(
                                f'{settings.BASE_URL}'
                                f'{
                                    reverse(
                                        'schedule:schedule',
                                        kwargs={'id': telegram_id},
                                    )
                                }'
                            ),
                        ),
                    ),
                ]],
            ),
        )
    return UserStates.SCHEDULE

schedule_handler = CommandHandler(schedule.__name__, schedule)
