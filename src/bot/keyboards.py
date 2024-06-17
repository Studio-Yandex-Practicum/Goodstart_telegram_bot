from django.conf import settings
from django.urls import reverse
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo


async def get_root_markup(telegram_id):
    keyboard = [
            [
                InlineKeyboardButton('Что умеет бот',
                                     callback_data="help"),
                InlineKeyboardButton(
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
            ],
        ]
    return InlineKeyboardMarkup(keyboard)
