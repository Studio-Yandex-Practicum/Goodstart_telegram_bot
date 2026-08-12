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


TRIAL_LESSON_CALLBACK_DATA = 'sign_up_trial_lesson'


def get_trial_lesson_markup():
    """Возвращает клавиатуру с кнопкой записи на пробный урок."""
    keyboard = [
        [
            InlineKeyboardButton(
                text='📝 Записаться на пробный урок',
                callback_data=TRIAL_LESSON_CALLBACK_DATA,
            ),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)
