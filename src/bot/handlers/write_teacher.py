from asgiref.sync import sync_to_async
from telegram import Update
from telegram.ext import CallbackQueryHandler, CommandHandler, ContextTypes

from core.logging import log_errors
from schooling.models import Student, Teacher
from bot.keyboards import WRITE_TEACHER_SELECT_PREFIX, get_write_teacher_markup
from bot.states import UserStates
from bot.utils import check_user_from_db

# TODO: перенести в bot/messages_texts/constants.py вместе с остальными
# текстами бота.
NO_TEACHER_MSG = 'За вами не закреплён преподаватель.'
STUDENT_ONLY_MSG = 'Эта функция доступна только ученикам.'
CHOOSE_TEACHER_MSG = 'Выберите преподавателя, которому хотите написать:'
ENTER_MESSAGE_MSG = (
    'Напишите сообщение для преподавателя {teacher_name}. '
    'Оно будет отправлено ему в чат с ботом.'
)
MESSAGE_SENT_MSG = 'Сообщение отправлено преподавателю ✅'
TEACHER_NOT_FOUND_MSG = (
    'Не удалось найти преподавателя. Попробуйте ещё раз.'
)

USER_DATA_TEACHER_ID_KEY = 'write_teacher_id'


async def get_student_teachers(student: Student) -> list[Teacher]:
    """
    Возвращает преподавателей, закреплённых за учеником.

    Преподаватель считается закреплённым за учеником, если учебный
    класс ученика присутствует в `study_classes` преподавателя.
    """
    if not student.study_class_id_id:
        return []
    return await sync_to_async(list)(
        Teacher.objects.filter(
            study_classes__id=student.study_class_id_id,
        ),
    )


async def get_student_teachers_by_lessons(student: Student) -> list[Teacher]:
    """
    Возвращает преподавателей, закреплённых за учеником.

    Преподаватель считается закреплённым за учеником, если у них есть
    хотя бы один общий урок (`Lesson`), где указаны и этот
    преподаватель, и этот ученик — то есть преподаватель когда-либо
    вёл или должен вести занятие у ученика.
    """
    return await sync_to_async(list)(
        Teacher.objects.filter(
            lessons__student_id_id=student.id,
        ).distinct(),
    )


@log_errors
async def write_teacher_start(
    update: Update, context: ContextTypes.DEFAULT_TYPE,
):
    """
    Точка входа в сценарий 'Написать преподавателю'.

    Проверяет, что пользователь — ученик, и что за ним закреплён
    хотя бы один преподаватель. Если преподаватель один — сразу
    предлагает написать сообщение. Если несколько — предлагает
    выбрать преподавателя из списка.
    """
    query = update.callback_query
    if query:
        await query.answer()

    telegram_id = update.effective_chat.id
    student = await check_user_from_db(telegram_id, (Student,))

    if not student:
        await context.bot.send_message(
            chat_id=telegram_id,
            text=STUDENT_ONLY_MSG,
        )
        return UserStates.START

    teachers = await get_student_teachers_by_lessons(student)

    if not teachers:
        await context.bot.send_message(
            chat_id=telegram_id,
            text=NO_TEACHER_MSG,
        )
        return UserStates.START

    if len(teachers) == 1:
        teacher = teachers[0]
        context.user_data[USER_DATA_TEACHER_ID_KEY] = teacher.id
        await context.bot.send_message(
            chat_id=telegram_id,
            text=ENTER_MESSAGE_MSG.format(
                teacher_name=f'{teacher.name} {teacher.surname}',
            ),
        )
        return UserStates.WRITE_TEACHER_MESSAGE

    await context.bot.send_message(
        chat_id=telegram_id,
        text=CHOOSE_TEACHER_MSG,
        reply_markup=get_write_teacher_markup(teachers),
    )
    return UserStates.WRITE_TEACHER


@log_errors
async def write_teacher_select(
    update: Update, context: ContextTypes.DEFAULT_TYPE,
):
    """Обрабатывает выбор конкретного преподавателя из списка."""
    query = update.callback_query
    await query.answer()

    teacher_id = int(query.data.split(':')[1])
    try:
        teacher = await Teacher.objects.aget(id=teacher_id)
    except Teacher.DoesNotExist:
        await query.message.reply_text(TEACHER_NOT_FOUND_MSG)
        return UserStates.START

    context.user_data[USER_DATA_TEACHER_ID_KEY] = teacher.id

    try:
        await query.edit_message_reply_markup(reply_markup=None)
    except Exception:
        pass

    await query.message.reply_text(
        ENTER_MESSAGE_MSG.format(
            teacher_name=f'{teacher.name} {teacher.surname}',
        ),
    )
    return UserStates.WRITE_TEACHER_MESSAGE


@log_errors
async def write_teacher_message(
    update: Update, context: ContextTypes.DEFAULT_TYPE,
):
    """Пересылает текстовое сообщение ученика выбранному преподавателю."""
    telegram_id = update.effective_chat.id
    teacher_id = context.user_data.get(USER_DATA_TEACHER_ID_KEY)

    if not teacher_id:
        # Пользователь оказался в этом состоянии без выбранного
        # преподавателя (например, после перезапуска бота) — начинаем
        # сценарий заново.
        return await write_teacher_start(update, context)

    student = await check_user_from_db(telegram_id, (Student,))
    try:
        teacher = await Teacher.objects.aget(id=teacher_id)
    except Teacher.DoesNotExist:
        await update.message.reply_text(TEACHER_NOT_FOUND_MSG)
        context.user_data.pop(USER_DATA_TEACHER_ID_KEY, None)
        return UserStates.START

    await context.bot.send_message(
        chat_id=teacher.telegram_id,
        text=(
            f'✉️ Сообщение от ученика {student.name} {student.surname}:\n\n'
            f'{update.message.text}'
        ),
    )
    await update.message.reply_text(MESSAGE_SENT_MSG)
    context.user_data.pop(USER_DATA_TEACHER_ID_KEY, None)
    return UserStates.START


# Отдельная top-level команда /write_teacher — на случай, если ученик
# захочет начать сценарий напрямую, а не через кнопку в корневой
# клавиатуре. Также используется как entry_point ConversationHandler'а.
write_teacher_handler = CommandHandler('write_teacher', write_teacher_start)

# Хендлер выбора преподавателя из списка (состояние WRITE_TEACHER).
write_teacher_select_handler = CallbackQueryHandler(
    write_teacher_select,
    pattern=rf'^{WRITE_TEACHER_SELECT_PREFIX}:\d+$',
)
