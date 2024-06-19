from telegram import Bot as TGBot
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from telegram.error import BadRequest
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.conf import settings

from .models import Lesson
from bot.bot_interface import Bot


async def send_lesson_end_notification(context: CallbackContext):
    bot = TGBot(token=settings.TELEGRAM_TOKEN)

    teacher_chat_id = context.job.data.get('teacher_chat_id')
    student_chat_id = context.job.data.get('student_chat_id')
    lesson_id = context.job.data.get('lesson_id')

    keyboard = [[
        InlineKeyboardButton('Да', callback_data=f'yes_{lesson_id}'),
        InlineKeyboardButton('Нет', callback_data=f'no_{lesson_id}'),
    ]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    message_text = 'Прошло ли занятие?'

    try:
        await bot.send_message(
            chat_id=teacher_chat_id,
            text=message_text,
            reply_markup=reply_markup
        )

        await bot.send_message(
            chat_id=student_chat_id,
            text=message_text,
            reply_markup=reply_markup
        )
    except BadRequest:
        print('Такой чат не найден!')


@receiver(post_save, sender=Lesson)
async def schedule_lesson_end_notification(sender, instance, **kwargs):
    bot = Bot()
    lesson_end_time = instance.datetime_end
    if lesson_end_time > timezone.now():
        bot._app.job_queue.run_once(
            send_lesson_end_notification,
            when=lesson_end_time,
            name=f'lesson_end_{instance.id}',
            data={
                'teacher_chat_id': instance.teacher_id.telegram_id,
                'student_chat_id': instance.student_id.telegram_id,
                'lesson_id': instance.id,
            }
        )
