import asyncio
from datetime import timedelta

from asgiref.sync import async_to_sync, sync_to_async
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
        reply_markup = async_to_sync(get_root_markup)(instance.telegram_id)
        send_message_to_user(settings.TELEGRAM_TOKEN,
                             instance.telegram_id,
                             message_text='Ваша заявка одобрена!',
                             reply_markup=reply_markup)


@receiver(post_save, sender=Lesson)
def notify_about_lesson(sender, instance, created, **kwargs):
    """Отправляет уведомление о времени занятия."""
    if created:
        message_text = (
            f'Ваше занятие назначено с {instance.datetime_start} '
            f'до {instance.datetime_end}.\n'
            f'Тема: {instance.name}'
        )
        if instance.teacher_id.telegram_id:
            reply_markup = async_to_sync(get_root_markup)(
                instance.teacher_id.telegram_id,
            )
        else:
            reply_markup = async_to_sync(get_root_markup)(
                instance.student_id.telegram_id,
            )
        send_message_to_user(settings.TELEGRAM_TOKEN,
                             instance.teacher_id.telegram_id,
                             message_text,
                             reply_markup=reply_markup)
        send_message_to_user(settings.TELEGRAM_TOKEN,
                             instance.student_id.telegram_id,
                             message_text,
                             reply_markup=reply_markup)


async def get_schedule_for_role(user):
    """Получение расписания пользователя в зависимости от роли."""
    if user.__class__.__name__ == 'Teacher':
        schedule = await sync_to_async(Lesson.objects.filter)(
            teacher_id=user.id,
        )
    else:
        schedule = await sync_to_async(Lesson.objects.filter)(
            student_id=user.id,
        )

    return schedule


async def get_schedule_for_day(schedule, start_week, day_offset):
    """Получение расписания пользователя в зависимости от дня."""
    target_date = start_week + timedelta(days=day_offset)

    return await sync_to_async(schedule.filter)(
        datetime_start__date=target_date,
    )


async def get_schedule_week_tasks(schedule, start_week):
    tasks = (
        get_schedule_for_day(schedule, start_week, 0),
        get_schedule_for_day(schedule, start_week, 1),
        get_schedule_for_day(schedule, start_week, 2),
        get_schedule_for_day(schedule, start_week, 3),
        get_schedule_for_day(schedule, start_week, 4),
        get_schedule_for_day(schedule, start_week, 5),
        get_schedule_for_day(schedule, start_week, 6),
    )
    return await asyncio.gather(*tasks)
