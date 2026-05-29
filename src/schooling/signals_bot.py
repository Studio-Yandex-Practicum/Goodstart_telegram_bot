import asyncio
import datetime
from typing import Optional
from datetime import timedelta

from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from telegram._utils.types import ReplyMarkup
from telegram.error import BadRequest, Forbidden
from asgiref.sync import sync_to_async
from django.conf import settings
from django.db.models.signals import post_save, post_init, post_delete
from django.dispatch import receiver
from loguru import logger
from pytz import timezone as pytz_timezone
from telegram.ext import Application

from bot.keyboards import get_root_markup
from schooling.constants import (LONG_TIME_REMINDER, SHORT_TIME_REMINDER,
                                 TIMEZONE_FOR_REMINDERS,)
from schooling.models import Student, Teacher, Lesson
from schooling.utils import format_datetime, format_lesson_duration


async def send_message_to_user(
    bot_token: str,
    user_id: int,
    message_text: str,
    reply_markup: Optional[ReplyMarkup] = None,
):
    """Инициативно отправляет сообщение."""
    bot = Bot(token=bot_token, base_url="http://195.133.8.27/bot")
    try:
        await bot.send_message(
            chat_id=user_id,
            text=message_text,
            parse_mode='HTML',
            reply_markup=reply_markup,
        )
    except Forbidden:
        logger.warning(
            f'Пропуск пользователя '
            f'Пользователь {user_id} заблокировал бота. ')
    except BadRequest as e:
        if 'Chat not found' in str(e):
            logger.warning(
                f'Пропуск пользователя '
                f'{user_id}: Чат не найден')


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
    lesson_id = context.job.data.get('lesson_id')

    keyboard = [[
        InlineKeyboardButton('✅ Да', callback_data=f'yes {lesson_id}'),
        InlineKeyboardButton('❌ Нет', callback_data=f'no {lesson_id}'),
    ]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    lesson = await Lesson.objects.select_related(
        'student_id',
    ).filter(id=int(lesson_id)).afirst()
    message_text = (
        f'📌 Подскажите, состоялось ли занятие по теме "{lesson.name}"?\n\n'
        'Выберите ответ ниже.'
    )

    chat_ids = (teacher_chat_id,)
    await gather_send_messages_to_users(
        chat_ids, message_text, reply_markup,
    )


# @receiver(post_save, sender=Lesson)
# async def schedule_lesson_end_notification(sender, instance, **kwargs):
#     """Создание задачи на отправку уведомления по окончании урока."""
#     from bot.bot_interface import Bot
#     if instance.is_passed:
#         return

#     bot = Bot()
#     app = await bot.get_app()
#     job_queue = app.job_queue

#     tz = pytz_timezone(TIMEZONE_FOR_REMINDERS)
#     lesson_end_time = instance.datetime_end.astimezone(tz)
#     if lesson_end_time > datetime.datetime.now(tz):
#         job_queue.run_once(
#             send_lesson_end_notification,
#             when=lesson_end_time,
#             name=f'lesson_end_{instance.id}',
#             data={
#                 'teacher_chat_id': await sync_to_async(
#                     lambda: instance.teacher_id.telegram_id,
#                 )(),
#                 'lesson_id': instance.id,
#             },
#         )


@receiver(post_save, sender=Teacher)
@receiver(post_save, sender=Student)
async def start_chat(sender, instance, created, **kwargs):
    """Отправляет уведомление об одобрении заявки."""
    if created:
        reply_markup = await get_root_markup(instance.telegram_id)
        await send_message_to_user(
            settings.TELEGRAM_TOKEN,
            instance.telegram_id,
            message_text='📌 Ваша заявка одобрена!',
            reply_markup=reply_markup,
        )


async def get_student_message_text(instance, is_notification=False):
    """Формируем сообщение для ученика с кликабельными ссылками."""
    start_time_formatted = format_datetime(instance.datetime_start)
    duration = format_lesson_duration(
        instance.datetime_start, instance.datetime_end)

    lesson_url = (f'{settings.BASE_URL}/schedule/'
                  f'{instance.student_id.telegram_id}/{instance.id}/')

    if is_notification:
        return (
            f'📌 Напоминание о занятии!\n\n'
            f'📖 Тема: {instance.name}\n'
            f'⏳ Начало в {instance.datetime_start.strftime('%H:%M')}\n'
            f'🔗 <b><a href="{instance.video_meeting_url}">'
            f'Ссылка на урок</a></b>\n'
        )

    return (
        f'📌 Вам назначено занятие!\n\n'
        f'📅 Дата: {start_time_formatted}\n'
        f'⏳ Длительность: {duration} минут\n'
        f'📖 Тема: {instance.name}\n'
        f'👨‍🏫 Преподаватель: {instance.teacher_id}\n'
        f'🔗 <b><a href="{instance.video_meeting_url}">'
        f'Ссылка на урок</a></b>\n\n'
        f'📚 <b><a href="{lesson_url}">'
        f'Домашнее задание можно будет найти тут</a></b>\n'
    )


async def get_homework_update_message(instance):
    """Формируем сообщение о обновлении домашнего задания."""
    lesson_url = (f'{settings.BASE_URL}/schedule/'
                  f'{instance.student_id.telegram_id}/{instance.id}/')

    return (
        f'📌 Домашнее задание обновлено!\n\n'
        f'👨‍🏫 Преподаватель: {instance.teacher_id}\n'
        f'📚 <b><a href="{lesson_url}">'
        f'Домашнее задание можно посмотреть тут</a></b>\n'
    )


async def get_teacher_message_text(instance, is_notification=False):
    """Формируем сообщение для учителя."""
    start_time_formatted = format_datetime(instance.datetime_start)
    duration = format_lesson_duration(
        instance.datetime_start, instance.datetime_end)

    lesson_url = (f'{settings.BASE_URL}/schedule/'
                  f'{instance.teacher_id.telegram_id}/{instance.id}/')

    if is_notification:
        return (
            f'📌 Напоминание о занятии!\n\n'
            f'📖 Тема: {instance.name}\n'
            f'⏳ Начало в {instance.datetime_start.strftime('%H:%M')}\n'
            f'🔗 <b><a href="{instance.video_meeting_url}">'
            f'Ссылка на урок</a></b>\n'
        )

    return (
    f'📌 Вам назначено занятие!\n\n'
    f'📅 Дата: {start_time_formatted}\n'
    f'⏳ Длительность: {duration} минут\n'
    f'📖 Тема: {instance.name}\n'
    f'🎓 Ученик: {instance.student_id}\n'
    f'🔗 <b><a href="{instance.video_meeting_url}">'
    f'Ссылка на урок</a></b>\n\n'
    f'📚 <b><a href="{lesson_url}">'
    f'Домашнее задание можно будет добавить тут</a></b>\n'
    )


async def send_notification(lesson, is_notification=False):
    """Отправляет уведомление о создании или напоминании о занятии."""
    student_message = await get_student_message_text(lesson, is_notification)
    teacher_message = await get_teacher_message_text(lesson, is_notification)

    student_telegram_id = await sync_to_async(
        lambda: lesson.student_id.telegram_id)()
    teacher_telegram_id = await sync_to_async(
        lambda: lesson.teacher_id.telegram_id)()

    if teacher_telegram_id:
        teacher_reply_markup = await get_root_markup(teacher_telegram_id)
        await gather_send_messages_to_users(
            chat_ids=[teacher_telegram_id],
            message_text=teacher_message,
            reply_markup=teacher_reply_markup,
        )

    if student_telegram_id:
        student_reply_markup = await get_root_markup(student_telegram_id)
        await gather_send_messages_to_users(
            chat_ids=[student_telegram_id],
            message_text=student_message,
            reply_markup=student_reply_markup,
        )


@receiver(post_init, sender=Lesson)
def init_lesson(sender, instance, **kwargs):
    if instance.id:
        instance.datetime_old = instance.datetime_start
        instance.teacher_old = instance.teacher_id


async def create_reminders(lesson, job_queue):
    """Создает задачи на напоминания о начале урока, не дублируя их."""
    tz = pytz_timezone(TIMEZONE_FOR_REMINDERS)
    lesson_time = lesson.datetime_start.astimezone(tz)
    reminders = [
        datetime.timedelta(minutes=LONG_TIME_REMINDER),
        datetime.timedelta(minutes=SHORT_TIME_REMINDER),
    ]

    for delta in reminders:
        reminder_time = lesson_time - delta
        if reminder_time > datetime.datetime.now(tz):
            job_queue.run_once(send_reminder, when=reminder_time, data=lesson)


async def send_reminder(context):
    """Функция отправки напоминания о занятии."""
    job = context.job
    lesson = job.data
    await send_notification(lesson, is_notification=True)


@receiver(post_save, sender=Lesson)
async def notify_about_lesson(sender, instance, created, **kwargs):
    """Создает задачи на напоминания, если урок только что создан."""
    from bot.bot_interface import Bot

    if created:
        await send_notification(instance)

        bot = Bot()
        app: Application = await bot.get_app()
        job_queue = app.job_queue

        await create_reminders(instance, job_queue)


@receiver(post_save, sender=Lesson)
async def msg_change_lesson(sender, instance, created, **kwargs):
    """Отправляет уведомление о изменении занятия."""
    message_text = ''  # Инициализация переменной
    if instance.is_passed:
        return
    if not created:
        start_time_formatted = format_datetime(instance.datetime_start)
        duration = format_lesson_duration(
            instance.datetime_start, instance.datetime_end)
        student_telegram_id = await sync_to_async(
            lambda: instance.student_id.telegram_id,
        )()
        teacher_old_telegram_id = None
        if instance.teacher_old:
            teacher_old_telegram_id = await sync_to_async(
                lambda: instance.teacher_old.telegram_id,
            )()
        chat_ids = (student_telegram_id, teacher_old_telegram_id)

        msg_text = (
            f'📌 Внимание!\n\n'
            f'Ваше занятие по теме "{instance.name}" '
            f'теперь будет проводить преподаватель {instance.teacher_id}.\n'
            f'📅 Дата: {start_time_formatted}\n'
            f'⏳ Длительность: {duration} минут.\n'
        )

        msg_student_old_teacher = (
                'Ваше занятие перенесено!\n\n'
                + msg_text
        )
        message_text = None

        if (
            instance.datetime_old != instance.datetime_start
            and instance.teacher_old != instance.teacher_id
        ):
            message_text = msg_student_old_teacher

        elif instance.datetime_old != instance.datetime_start:
            message_text = (
                f'📌 Занятие по теме "{instance.name}" перенесено!\n\n'
                f'📅 Новая дата: {start_time_formatted}\n'
                f'⏳ Длительность: {duration} минут.\n'
            )
            chat_ids = (
                await sync_to_async(lambda: instance.student_id.telegram_id)(),
                await sync_to_async(lambda: instance.teacher_id.telegram_id)(),
            )

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

        if message_text is not None:
            await gather_send_messages_to_users(
                chat_ids=chat_ids,
                message_text=message_text,
                reply_markup=reply_markup,
            )


@receiver(post_delete, sender=Lesson)
async def delete_lesson_and_send_msg(sender, instance, *args, **kwargs):
    """Отправляет уведомление об отмене занятия."""
    from bot.bot_interface import Bot
    bot = Bot()
    app = await bot.get_app()
    job_queue = app.job_queue
    # Удаляем все задачи, связанные с этим занятием
    for job in job_queue.jobs():
        if (job.data and isinstance(job.data, dict) and
        job.data.get('lesson_id') == instance.id):
            job.schedule_removal()
    if instance.is_passed:
        return
    if instance.teacher_id is None:
        return
    start_time_formatted = format_datetime(instance.datetime_start)
    duration = format_lesson_duration(
        instance.datetime_start, instance.datetime_end)
    student_telegram_id = await sync_to_async(
        lambda: instance.student_id.telegram_id,
    )()
    teacher_telegram_id = await sync_to_async(
        lambda: instance.teacher_id.telegram_id,
    )()
    chat_ids = (student_telegram_id, teacher_telegram_id)
    message_text = (
        f'📌 Занятие отменено!\n\n'
        f'Тема: "{instance.name}"\n'
        f'📅 Дата: {start_time_formatted}\n'
        f'⏳ Длительность: {duration} минут.\n'
    )

    if instance.teacher_id.telegram_id:
        reply_markup = await get_root_markup(instance.teacher_id.telegram_id)
    else:
        reply_markup = await get_root_markup(instance.student_id.telegram_id)

    await gather_send_messages_to_users(
        chat_ids=chat_ids,
        message_text=message_text,
        reply_markup=reply_markup,
    )


async def get_schedule_for_role(user):
    """Получает расписание пользователя в зависимости от его роли."""
    if await Teacher.objects.filter(id=user.id).aexists():
        schedule = await sync_to_async(list)(
            Lesson.objects.filter(teacher_id=user.id)
            .select_related('student_id', 'teacher_id', 'subject')
            .only('id', 'name', 'datetime_start', 'duration',
                  'subject_id', 'teacher_id', 'student_id',),
        )
    else:
        schedule = await sync_to_async(list)(
            Lesson.objects.filter(student_id=user.id)
            .select_related('student_id', 'teacher_id', 'subject')
            .only('id', 'name', 'datetime_start', 'duration',
                  'subject_id', 'teacher_id', 'student_id',),
        )
    return schedule


async def get_schedule_for_day(schedule, start_week, day_offset):
    """Фильтрует расписание по конкретному дню недели."""
    target_date = start_week + timedelta(days=day_offset)
    return [lesson for lesson in schedule
            if lesson.datetime_start.date() == target_date]


async def get_schedule_week_tasks(schedule, start_week):
    """Создает задачи для получения расписания на всю неделю."""
    tasks = [get_schedule_for_day(schedule, start_week, i) for i in range(7)]
    return await asyncio.gather(*tasks)
