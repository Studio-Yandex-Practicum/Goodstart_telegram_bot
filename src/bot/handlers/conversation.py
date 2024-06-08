from typing import Optional

from telegram import Update
from telegram.ext import CallbackContext

from bot.states import UserStates
from core.logging import log_errors


@log_errors
async def help(
    update: Update,
    context: CallbackContext,
) -> Optional[UserStates]:
    """Обработчик кнопки "help"."""
    query = update.callback_query
    if query:
        await query.answer()
        await query.edit_message_text(text='Вы нажали Помощь',
                                      reply_markup=None)
        return UserStates.HELP
    return None


@log_errors
async def schedule(update: Update,
                   context: CallbackContext) -> Optional[UserStates]:
    """Обработчик кнопки "Расписание"."""
    query = update.callback_query
    if query:
        await query.answer()
        await query.edit_message_text(text='Вы нажали Расписание',
                                      reply_markup=None)
        return UserStates.SCHEDULE
    return None
