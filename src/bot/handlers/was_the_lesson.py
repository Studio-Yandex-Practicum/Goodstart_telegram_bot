# TODO: Нам не нужен этот хендлер в виде команды. Он нам нужен как обработчик
from asgiref.sync import sync_to_async
from telegram import (
    Update, KeyboardButton, ReplyKeyboardMarkup,
)
from telegram.ext import CallbackContext, CallbackQueryHandler

from schooling.models import Lesson, Student
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

    lesson = await Lesson.objects.select_related('teacher_id',).aget(
        id=int(lesson_id),
    )

    teacher_tg_id = await sync_to_async(
        lambda: lesson.teacher_id.telegram_id)()
    student_tg_id = await sync_to_async(
        lambda: lesson.student_id.telegram_id)()

    context.user_data.setdefault('lesson_responses', {})

    if query.from_user.id == teacher_tg_id:
        context.user_data['lesson_responses']['teacher_answ'] = response

    teacher_answ = (
        context.user_data['lesson_responses'].get('teacher_answ')
    )

    if teacher_answ == 'yes':
        lesson.is_passed_teacher = True
        await lesson.asave()
        await query.edit_message_text(
            text=SUCCESS_LESSON_MSG,
        )

    if lesson.is_passed_teacher:
        lesson.is_passed = True
        await lesson.asave()
        student = await Student.objects.aget(telegram_id=student_tg_id)
        student.paid_lessons -= 1
        await student.asave()
        context.user_data['lesson_responses'].clear()

    if teacher_answ == 'no':
        await no_answ_lesson_response(
                query=query,
                update=update,
            )


lesson_end_handler = CallbackQueryHandler(was_the_lesson_completed)
