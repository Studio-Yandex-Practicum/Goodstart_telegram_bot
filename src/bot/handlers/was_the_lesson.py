# TODO: Нам не нужен этот хендлер в виде команды. Он нам нужен как обработчик
from telegram import (
    Update, KeyboardButton, ReplyKeyboardMarkup,
)
from telegram.ext import CallbackContext, CallbackQueryHandler

from schooling.models import Lesson
from bot.states import UserStates
from bot.messages_texts.constants import (
    UNCOMPLETED_LESSON_FEEDBACK_MSG,
    SUCCESS_LESSON_MSG,
)


async def no_answ_lesson_response(query, update):
    keyboard = [[KeyboardButton('/feedback')]]
    reply_markup = ReplyKeyboardMarkup(
        keyboard,
        one_time_keyboard=True,
        resize_keyboard=True,
    )
    message = (
        query.message if
        query.message else
        update.callback_query.message
    )
    await message.reply_text(
        UNCOMPLETED_LESSON_FEEDBACK_MSG,
        reply_markup=reply_markup,
    )


async def was_the_lesson_completed(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    if query.data == 'help':
        return UserStates.HELP

    response, lesson_id = query.data.split()
    user_id = query.from_user.id

    lesson = await Lesson.objects.select_related(
        'teacher_id', 'student_id',
    ).aget(
        id=int(lesson_id),
    )

    teacher_tg_id = lesson.teacher_id.telegram_id
    student_tg_id = lesson.student_id.telegram_id

    context.user_data.setdefault('lesson_responses', {})

    if user_id == teacher_tg_id:
        context.user_data['lesson_responses']['teacher_answ'] = response
    elif user_id == student_tg_id:
        context.user_data['lesson_responses']['student_answ'] = response

    teacher_answ = (
        context.user_data['lesson_responses'].get('teacher_answ')
    )
    student_answ = (
        context.user_data['lesson_responses'].get('student_answ')
    )

    if teacher_answ == 'yes':
        lesson.is_passed_teacher = True
        await lesson.asave()

    if student_answ == 'yes':
        lesson.is_passed_student = True
        await lesson.asave()

    if lesson.is_passed_teacher and lesson.is_passed_student:
        lesson.is_passed = True
        await lesson.asave()
        context.user_data['lesson_responses'].clear()

    elif teacher_answ == 'no' or student_answ == 'no':
        await no_answ_lesson_response(
                query=query,
                update=update,
            )

    else:
        await query.edit_message_text(
            text=SUCCESS_LESSON_MSG,
        )

lesson_end_handler = CallbackQueryHandler(was_the_lesson_completed)
