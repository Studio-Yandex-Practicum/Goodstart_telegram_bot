from django.conf import settings
from django.urls import reverse
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

from bot.states import UserStates


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
        [
            InlineKeyboardButton(
                text='✉️ Написать преподавателю',
                callback_data=UserStates.WRITE_TEACHER.value,
            ),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


WRITE_TEACHER_SELECT_PREFIX = 'write_teacher_select'


def get_write_teacher_markup(teachers):
    """Возвращает клавиатуру с выбором преподавателя из списка."""
    keyboard = [
        [
            InlineKeyboardButton(
                text=f'{teacher.name} {teacher.surname}',
                callback_data=(
                    f'{WRITE_TEACHER_SELECT_PREFIX}:{teacher.id}'
                ),
            ),
        ]
        for teacher in teachers
    ]
    return InlineKeyboardMarkup(keyboard)


TRIAL_LESSON_CALLBACK_DATA = 'sign_up_trial_lesson'


def get_trial_lesson_markup():
    """Возвращает клавиатуру с кнопкой записи на пробный урок."""
    keyboard = [
        [
            InlineKeyboardButton(
                text='📝 Записаться',
                callback_data=TRIAL_LESSON_CALLBACK_DATA,
            ),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)
