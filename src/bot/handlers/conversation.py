from typing import Optional

from telegram import Update
from telegram.ext import CallbackContext

from schooling.models import Teacher, Student
from bot.states import UserStates, UserFlow
from bot.utils import check_user_from_db
from core.logging import log_errors


@log_errors
async def help(
    update: Update,
    context: CallbackContext,
) -> Optional[UserStates]:
    """Обработчик кнопки "help"."""
    query = update.callback_query
    if query:
        user = await check_user_from_db(
            telegram_id=query.from_user.id,
            from_models=(Teacher, Student),
        )
        user_flow = UserFlow(user)
        await user_flow.help()
        await query.answer()
        await query.edit_message_text(text='Вы нажали Помощь',
                                      reply_markup=None)
        return user_flow.state
    return None


@log_errors
async def schedule(update: Update,
                   context: CallbackContext) -> Optional[UserStates]:
    """Обработчик кнопки "Расписание"."""
    query = update.callback_query
    if query:
        user = await check_user_from_db(
            telegram_id=query.from_user.id,
            from_models=(Teacher, Student),
        )
        user_flow = UserFlow(user)
        await user_flow.schedule()
        await query.answer()
        await query.edit_message_text(text='Вы нажали Расписание',
                                      reply_markup=None)
        return user_flow.state
    return None
