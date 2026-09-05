from asgiref.sync import sync_to_async
from loguru import logger
from telegram import Update
from telegram.error import BadRequest, Forbidden
from telegram.ext import CallbackQueryHandler, CommandHandler, ContextTypes

from core.logging import log_errors
from schooling.models import Student, Teacher
from schooling.services.conversation import record_conversation_message_async
from bot.keyboards import WRITE_STUDENT_SELECT_PREFIX, get_write_student_markup
from bot.states import UserStates
from bot.utils import check_user_from_db

# TODO: перенести в bot/messages_texts/constants.py вместе с остальными
# текстами бота.
NO_STUDENT_MSG = 'За вами не закреплено ни одного ученика.'
TEACHER_ONLY_MSG = 'Эта функция доступна только преподавателям.'
CHOOSE_STUDENT_MSG = 'Выберите ученика, которому хотите написать:'
ENTER_MESSAGE_MSG = (
    'Напишите сообщение для ученика {student_name}. '
    'Оно будет отправлено ему в чат с ботом.'
)
MESSAGE_SENT_MSG = 'Сообщение отправлено ученику ✅'
STUDENT_NOT_FOUND_MSG = 'Не удалось найти ученика. Попробуйте ещё раз.'
STUDENT_CHAT_UNAVAILABLE_MSG = (
    'Не удалось доставить сообщение: похоже, ученик заблокировал '
    'чат с ботом или ещё не запускал его. Свяжитесь с ним '
    'другим способом или обратитесь в поддержку.'
)

USER_DATA_STUDENT_ID_KEY = 'write_student_id'


async def get_teacher_students_by_lessons(teacher: Teacher) -> list[Student]:
    """
    Возвращает учеников, закреплённых за преподавателем.

    Преподаватель считается закреплённым за учеником, если у них есть
    хотя бы один общий урок (`Lesson`), где указаны и этот
    преподаватель, и этот ученик.
    """
    return await sync_to_async(list)(
        Student.objects.filter(
            lessons__teacher_id_id=teacher.id,
        ).distinct(),
    )


@log_errors
async def write_student_start(
    update: Update, context: ContextTypes.DEFAULT_TYPE,
):
    """
    Точка входа в сценарий 'Написать ученику'.

    Проверяет, что пользователь — преподаватель, и что за ним
    закреплён хотя бы один ученик. Если ученик один — сразу
    предлагает написать сообщение. Если несколько — предлагает
    выбрать ученика из списка.
    """
    query = update.callback_query
    if query:
        await query.answer()

    telegram_id = update.effective_chat.id
    teacher = await check_user_from_db(telegram_id, (Teacher,))

    if not teacher:
        await context.bot.send_message(
            chat_id=telegram_id,
            text=TEACHER_ONLY_MSG,
        )
        return UserStates.START

    students = await get_teacher_students_by_lessons(teacher)

    if not students:
        await context.bot.send_message(
            chat_id=telegram_id,
            text=NO_STUDENT_MSG,
        )
        return UserStates.START

    if len(students) == 1:
        student = students[0]
        context.user_data[USER_DATA_STUDENT_ID_KEY] = student.id
        await context.bot.send_message(
            chat_id=telegram_id,
            text=ENTER_MESSAGE_MSG.format(
                student_name=f'{student.name} {student.surname}',
            ),
        )
        return UserStates.WRITE_STUDENT_MESSAGE

    await context.bot.send_message(
        chat_id=telegram_id,
        text=CHOOSE_STUDENT_MSG,
        reply_markup=get_write_student_markup(students),
    )
    return UserStates.WRITE_STUDENT


@log_errors
async def write_student_select(
    update: Update, context: ContextTypes.DEFAULT_TYPE,
):
    """Обрабатывает выбор конкретного ученика из списка."""
    query = update.callback_query
    await query.answer()

    student_id = int(query.data.split(':')[1])
    try:
        student = await Student.objects.aget(id=student_id)
    except Student.DoesNotExist:
        await query.message.reply_text(STUDENT_NOT_FOUND_MSG)
        return UserStates.START

    context.user_data[USER_DATA_STUDENT_ID_KEY] = student.id

    try:
        await query.edit_message_reply_markup(reply_markup=None)
    except Exception:
        pass

    await query.message.reply_text(
        ENTER_MESSAGE_MSG.format(
            student_name=f'{student.name} {student.surname}',
        ),
    )
    return UserStates.WRITE_STUDENT_MESSAGE


@log_errors
async def write_student_message(
    update: Update, context: ContextTypes.DEFAULT_TYPE,
):
    """Пересылает текстовое сообщение преподавателя выбранному ученику."""
    telegram_id = update.effective_chat.id
    student_id = context.user_data.get(USER_DATA_STUDENT_ID_KEY)

    if not student_id:
        # Пользователь оказался в этом состоянии без выбранного
        # ученика (например, после перезапуска бота) — начинаем
        # сценарий заново.
        return await write_student_start(update, context)

    teacher = await check_user_from_db(telegram_id, (Teacher,))
    try:
        student = await Student.objects.aget(id=student_id)
    except Student.DoesNotExist:
        await update.message.reply_text(STUDENT_NOT_FOUND_MSG)
        context.user_data.pop(USER_DATA_STUDENT_ID_KEY, None)
        return UserStates.START

    try:
        await context.bot.send_message(
            chat_id=student.telegram_id,
            text=(
                f'✉️ Сообщение от преподавателя '
                f'{teacher.name} {teacher.surname}:\n\n'
                f'{update.message.text}'
            ),
        )
    except (BadRequest, Forbidden) as e:
        # BadRequest('Chat not found') — ученик никогда не запускал
        # бота (нет чата с ним). Forbidden — ученик заблокировал
        # бота. Обе ситуации не даём преподавателю улетать в никуда,
        # а сообщаем о недоставке.
        logger.warning(
            f'Не удалось отправить сообщение ученику '
            f'{student.id} ({student.telegram_id}): {e}',
        )
        await update.message.reply_text(STUDENT_CHAT_UNAVAILABLE_MSG)
        context.user_data.pop(USER_DATA_STUDENT_ID_KEY, None)
        return UserStates.START

    await record_conversation_message_async(
        teacher, student,
        f'Преподаватель {teacher.name} {teacher.surname}',
        update.message.text,
    )

    await update.message.reply_text(MESSAGE_SENT_MSG)
    context.user_data.pop(USER_DATA_STUDENT_ID_KEY, None)
    return UserStates.START


# Отдельная top-level команда /write_student — на случай, если
# преподаватель захочет начать сценарий напрямую, а не через кнопку в
# корневой клавиатуре. Также используется как entry_point
# ConversationHandler'а.
write_student_handler = CommandHandler('write_student', write_student_start)

# Хендлер выбора ученика из списка (состояние WRITE_STUDENT).
write_student_select_handler = CallbackQueryHandler(
    write_student_select,
    pattern=rf'^{WRITE_STUDENT_SELECT_PREFIX}:\d+$',
)
