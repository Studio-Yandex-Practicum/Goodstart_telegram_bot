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
from django.db.models.signals import post_save, post_init, pre_delete
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


async def get_message_text(instance):
    """Получаем сообщение о назначении урока."""
    message_text = (
            f'Вам назначено занятие с {instance.datetime_start} '
            f'до {instance.datetime_end}.\n'
            f'Тема: {instance.name}.\n'
            f'Преподаватель: {instance.teacher_id}\n'
            f'Ученик: {instance.student_id}\n'
        )
    test_msg = f'{instance._meta.get_field('test_lesson').verbose_name}'
    if instance.test_lesson:
        message_text = message_text + test_msg
    return message_text


@receiver(post_init, sender=Lesson)
def init_lesson(sender, instance, **kwargs):
    instance.datetime_old = instance.datetime_start  # до изменения возникала ошибка при генерации уроков
    instance.teacher_old = instance.teacher_id


@receiver(post_save, sender=Lesson)
async def notify_about_lesson(sender, instance, created, **kwargs):
    """Отправляет уведомление о времени занятия."""
    if created:
        message_text = await get_message_text(instance)

        if instance.teacher_id.telegram_id:
            reply_markup = await get_root_markup(
                instance.teacher_id.telegram_id,
            )
        else:
            reply_markup = await get_root_markup(
                instance.student_id.telegram_id,
            )

        chat_ids = (
                instance.student_id.telegram_id,
                instance.teacher_id.telegram_id,
            )

        await gather_send_messages_to_users(
            chat_ids=chat_ids,
            message_text=message_text,
            reply_markup=reply_markup,
        )


@receiver(post_save, sender=Lesson)
async def msg_change_lesson(sender, instance, created, **kwargs):
    """Отправляет уведомление о изменении занятия."""
    if not created:
        chat_ids = (
                instance.student_id.telegram_id,
                instance.teacher_old.telegram_id,
            )
        chat_id = instance.teacher_id.telegram_id
        msg_teacher = await get_message_text(instance)
        msg_text = (
            f'Ваше занятие на тему "{instance.name}" '
            f'проведёт преподаватель {instance.teacher_id}\n'
            f'{instance.datetime_start.date()} c '
            f'{instance.datetime_start.time()} до '
            f'{instance.datetime_end.time()}.'
        )
        msg_student_old_teacher = 'Ваше занятие перенесено!\n' + msg_text

        if (
            instance.datetime_old != instance.datetime_start
            and instance.teacher_old != instance.teacher_id
        ):
            message_text = msg_student_old_teacher

        elif instance.datetime_old != instance.datetime_start:
            message_text = (
                f'Занятие на тему "{instance.name}" перенесено '
                f'на {instance.datetime_start.date()} c '
                f'{instance.datetime_start.time()} до '
                f'{instance.datetime_end.time()}.'
            )
            chat_ids = (
                instance.student_id.telegram_id,
                instance.teacher_id.telegram_id,
            )
            chat_id = None

        elif instance.teacher_old != instance.teacher_id:
            message_text = msg_text

        if instance.teacher_id.telegram_id:
            reply_markup = await get_root_markup(
                instance.teacher_id.telegram_id,
            )
        elif instance.teacher_old.telegram_id:
            reply_markup = await get_root_markup(
                instance.teacher_old.telegram_id,
            )
        else:
            reply_markup = await get_root_markup(
                instance.student_id.telegram_id,
            )

        await gather_send_messages_to_users(
            chat_ids=chat_ids,
            message_text=message_text,
            reply_markup=reply_markup,
        )
        if chat_id:
            bot_token = settings.TELEGRAM_TOKEN
            await send_message_to_user(
                bot_token, chat_id, msg_teacher, reply_markup,
            )


@receiver(pre_delete, sender=Lesson)
async def delete_lesson_and_send_msg(sender, instance, *args, **kwargs):
    """Отправляет уведомление об отмене занятия."""
    chat_ids = (
        instance.student_id.telegram_id,
        instance.teacher_id.telegram_id,
    )
    message_text = (
        f'Занятие на тему "{instance.name}" '
        f'{instance.datetime_start.date()} c '
        f'{instance.datetime_start.time()} до '
        f'{instance.datetime_end.time()} отменено.'
    )
    if instance.teacher_id.telegram_id:
            reply_markup = await get_root_markup(
                instance.teacher_id.telegram_id,
            )
    else:
        reply_markup = await get_root_markup(
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
