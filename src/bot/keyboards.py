from django.conf import settings
from django.urls import reverse
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo


async def get_root_markup(telegram_id):
    """Возвращает клавиатуру с кнопкой для просмотра расписания."""
    schedule_url = f"{settings.BASE_URL}{reverse(
        'schedule:schedule',
        kwargs={'id': telegram_id}
    )}"

    keyboard = [
        [
            InlineKeyboardButton(
                text='📜 Посмотреть расписание',
                web_app=WebAppInfo(url=schedule_url),
            ),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)
