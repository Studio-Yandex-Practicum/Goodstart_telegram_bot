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
    WELCOME_MSG, REGISTRATION_MSG, APPLICATION_EXISTS_MSG, UNKNOWN_USER_HELP_MSG,
)
from bot.keyboards import get_root_markup
from bot.states import UserStates


@log_errors
async def left_lessons(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    """
    `/left_lessons` command handler.

    If the user is registered in the database and role student, sends message,
    with left payed lessons.
    """

    telegram_id = update.effective_chat.id
    user = await check_user_from_db(telegram_id, (Teacher, Student))
    if not user or user.__class__.__name__ != 'Student':
        await context.bot.send_message(
            chat_id=telegram_id,
            text='Эта функция доступна только для учеников.',
        )
    else:
        left = user.paid_lessons
        if left == 0 or left > 4:
            lesson = 'занятий'
        else:
            lesson = 'занятия'
        await update.message.reply_text(
            f'{user.name}, у вас осталось {user.paid_lessons} оплаченных {lesson}.',
        )
    return UserStates.START

left_lessons_handler = CommandHandler(left_lessons.__name__, left_lessons,)
