from django.conf import settings
from django.urls import reverse
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

from bot.states import UserStates


async def get_root_markup(telegram_id, user=None):
    """
    Возвращает клавиатуру с кнопкой для просмотра расписания.

    Также добавляет кнопку переписки: ученику — 'Написать
    преподавателю', преподавателю — 'Написать ученику'. Если `user`
    (объект `Teacher`/`Student`) не передан, роль определяется
    поиском по `telegram_id` в базе.
    """
    if user is None:
        from bot.utils import check_user_from_db
        from schooling.models import Student, Teacher
        user = await check_user_from_db(telegram_id, (Teacher, Student))

    is_teacher = user is not None and user.__class__.__name__ == 'Teacher'

    schedule_url = f"{settings.BASE_URL}{reverse(
        'schedule:schedule',
        kwargs={'id': telegram_id}
    )}"

    write_button = (
        InlineKeyboardButton(
            text='✉️ Написать ученику',
            callback_data=UserStates.WRITE_STUDENT.value,
        )
        if is_teacher
        else InlineKeyboardButton(
            text='✉️ Написать преподавателю',
            callback_data=UserStates.WRITE_TEACHER.value,
        )
    )

    keyboard = [
        [
            InlineKeyboardButton(
                text='📜 Посмотреть расписание',
                web_app=WebAppInfo(url=schedule_url),
            ),
        ],
        [write_button],
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


WRITE_STUDENT_SELECT_PREFIX = 'write_student_select'


def get_write_student_markup(students):
    """Возвращает клавиатуру с выбором ученика из списка."""
    keyboard = [
        [
            InlineKeyboardButton(
                text=f'{student.name} {student.surname}',
                callback_data=(
                    f'{WRITE_STUDENT_SELECT_PREFIX}:{student.id}'
                ),
            ),
        ]
        for student in students
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
