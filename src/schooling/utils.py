from asgiref.sync import async_to_sync
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from telegram import Bot
from telegram.error import BadRequest

from bot.keyboards import get_root_markup
from schooling.models import Student, Teacher, Lesson


@async_to_sync
async def send_message_to_user(bot_token, user_id,
                               message_text,
                               reply_markup=None):
    """Инициативно отправляет сообщение."""
    bot = Bot(token=bot_token)
    try:
        await bot.send_message(chat_id=user_id,
                               text=message_text,
                               reply_markup=reply_markup)
    except BadRequest:
        print('Такой чат не найден!')


@receiver(post_save, sender=Teacher)
@receiver(post_save, sender=Student)
def start_chat(sender, instance, created, **kwargs):
    """Отправляет уведомление об одобрении заявки."""
    if created:
        reply_markup = async_to_sync(get_root_markup)()
        send_message_to_user(settings.TELEGRAM_TOKEN,
                             instance.telegram_id,
                             message_text='Ваша заявка одобрена!',
                             reply_markup=reply_markup)


@receiver(post_save, sender=Lesson)
def notify_about_lesson(sender, instance, created, **kwargs):
    """Отправляет уведомление о времени занятия."""
    if created:
        message_text = f"""Ваше занятие назначено с {instance.datetime_start}
                           до {instance.datetime_end}.
                           Тема: {instance.name}"""
        reply_markup = async_to_sync(get_root_markup)()
        send_message_to_user(settings.TELEGRAM_TOKEN,
                             instance.teacher_id,
                             message_text,
                             reply_markup)
        send_message_to_user(settings.TELEGRAM_TOKEN,
                             instance.student_id,
                             message_text,
                             reply_markup)
