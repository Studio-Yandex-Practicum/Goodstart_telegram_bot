from telegram import Update
from telegram.ext import CallbackContext, CallbackQueryHandler
from schooling.models import Lesson


async def button(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    lesson_id = int(query.data.split('_')[-1])
    response = query.data.split('_')[0]
    user_id = query.from_user.id

    try:
        lesson = await Lesson.objects.select_related(
            'teacher_id', 'student_id',
        ).aget(id=lesson_id)

        context.user_data.setdefault('lesson_responses', {})

        if user_id == lesson.teacher_id.telegram_id:
            context.user_data['lesson_responses']['teacher_answ'] = response
        elif user_id == lesson.student_id.telegram_id:
            context.user_data['lesson_responses']['student_answ'] = response

        teacher_answ = context.user_data['lesson_responses'].get('teacher_answ')
        student_answ = context.user_data['lesson_responses'].get('student_answ')

        print(teacher_answ)
        print(student_answ)

        if teacher_answ is not None and student_answ is not None:
            if teacher_answ == 'yes' and student_answ == 'yes':
                lesson.is_passed = True
                await lesson.asave()
                await query.edit_message_text(text='Занятие завершено.')
                context.user_data['lesson_responses'].clear()
        else:
            await query.edit_message_text(text='Ответ получен.')

    except Lesson.DoesNotExist:
        await query.edit_message_text(text='Занятие не найдено.')


lesson_end_handler = CallbackQueryHandler(button)
