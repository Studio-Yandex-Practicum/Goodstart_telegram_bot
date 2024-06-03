from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from bot.states import States


async def get_root_markup():
    keyboard = [
            [
                InlineKeyboardButton('Что умеет бот',
                                     callback_data=States.HELP.value),
                InlineKeyboardButton('Посмотреть расписание',
                                     callback_data=States.SCHEDULE.value),
            ],
        ]
    return InlineKeyboardMarkup(keyboard)
