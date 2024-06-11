from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from bot.states import UserStates


async def get_root_markup():
    keyboard = [
            [
                InlineKeyboardButton('Что умеет бот',
                                     callback_data=UserStates.HELP.value),
                InlineKeyboardButton('Посмотреть расписание',
                                     callback_data=UserStates.SCHEDULE.value),
            ],
        ]
    return InlineKeyboardMarkup(keyboard)
