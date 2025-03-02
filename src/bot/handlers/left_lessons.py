# TODO: должна отображаться только ученикам
from telegram import (
    Update,
)
from telegram.ext import CommandHandler, ContextTypes

from core.logging import log_errors
from schooling.models import Teacher, Student
from bot.utils import check_user_from_db

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
            text=(
                '📌 Внимание!\n\n'
                'Эта функция доступна только для учеников.'
            ),
        )
    else:
        left = user.paid_lessons
        if left == 0 or left > 4:
            lesson = 'занятий'
        else:
            lesson = 'занятия'
        await update.message.reply_text(
            f'📌 {user.name}!\n\n'
            f'У вас осталось {user.paid_lessons} оплаченных {lesson}.',
        )
    return UserStates.START

left_lessons_handler = CommandHandler(left_lessons.__name__, left_lessons,)
