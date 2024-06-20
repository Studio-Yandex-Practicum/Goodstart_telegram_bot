import asyncio
from typing import Optional
from datetime import timedelta

from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from telegram._utils.types import ReplyMarkup
from telegram.error import BadRequest
from django.utils import timezone
from asgiref.sync import sync_to_async
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from bot.keyboards import get_root_markup
from schooling.models import Student, Teacher, Lesson


async def send_message_to_user(
    bot_token: str,
    user_id: int,
    message_text: str,
    reply_markup: Optional[ReplyMarkup] = None,
):
    """Инициативно отправляет сообщение."""
    bot = Bot(token=bot_token)
    try:
        await bot.send_message(
            chat_id=user_id,
            text=message_text,
            reply_markup=reply_markup,
        )
    except BadRequest:
        print(f'Чат с id {user_id} не найден!')


async def gather_send_messages_to_users(
    chat_ids: list[int],
    message_text: str,
    reply_markup: Optional[ReplyMarkup] = None,
):
    """Создание задачи на отправку сообщения нескольким пользователям."""
    bot_token = settings.TELEGRAM_TOKEN
    tasks = [
        send_message_to_user(
            bot_token, chat_id, message_text, reply_markup,
        ) for chat_id in chat_ids
    ]
    await asyncio.gather(*tasks)


async def send_lesson_end_notification(context: CallbackContext):
    """Отправка сообщения с выбором 'Да' / 'Нет' прошло ли занятие."""
    teacher_chat_id = context.job.data.get('teacher_chat_id')
    student_chat_id = context.job.data.get('student_chat_id')
    lesson_id = context.job.data.get('lesson_id')

    keyboard = [[
        InlineKeyboardButton('Да', callback_data=f'yes {lesson_id}'),
        InlineKeyboardButton('Нет', callback_data=f'no {lesson_id}'),
    ]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    message_text = 'Было ли занятие?'

    chat_ids = (teacher_chat_id, student_chat_id)
    await gather_send_messages_to_users(
        chat_ids, message_text, reply_markup,
    )


@receiver(post_save, sender=Lesson)
async def schedule_lesson_end_notification(sender, instance, **kwargs):
    """Создание задачи на отправку уведомления по окончании урока."""
    from bot.bot_interface import Bot
    bot = Bot()
    app = await bot.get_app()
    lesson_end_time = instance.datetime_end
    if lesson_end_time > timezone.now():
        try:
            app.job_queue.run_once(
                send_lesson_end_notification,
                when=lesson_end_time,
                name=f'lesson_end_{instance.id}',
                data={
                    'teacher_chat_id': instance.teacher_id.telegram_id,
                    'student_chat_id': instance.student_id.telegram_id,
                    'lesson_id': instance.id,
                },
            )
        except AttributeError as error:
            print(f'Ошибка: {error}')


@receiver(post_save, sender=Teacher)
@receiver(post_save, sender=Student)
async def start_chat(sender, instance, created, **kwargs):
    """Отправляет уведомление об одобрении заявки."""
    if created:
        reply_markup = await get_root_markup(instance.telegram_id)
        await send_message_to_user(
            settings.TELEGRAM_TOKEN,
            instance.telegram_id,
            message_text='Ваша заявка одобрена!',
            reply_markup=reply_markup,
        )


@receiver(post_save, sender=Lesson)
async def notify_about_lesson(sender, instance, created, **kwargs):
    """Отправляет уведомление о времени занятия."""
    if created:
        message_text = (
            f'Ваше занятие назначено с {instance.datetime_start} '
            f'до {instance.datetime_end}.\n'
            f'Тема: {instance.name}'
        )
        if instance.teacher_id.telegram_id:
            reply_markup = await get_root_markup(
                instance.teacher_id.telegram_id,
            )
        else:
            reply_markup = await get_root_markup(
                instance.student_id.telegram_id,
            )

        chat_ids = (
            instance.teacher_id.telegram_id,
            instance.student_id.telegram_id,
        )
        await gather_send_messages_to_users(
            chat_ids=chat_ids,
            message_text=message_text,
            reply_markup=reply_markup,
        )


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
