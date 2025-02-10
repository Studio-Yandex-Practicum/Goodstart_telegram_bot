from asgiref.sync import sync_to_async
import pytz
from django.conf import settings
from django.core.mail import send_mail
from django.db import IntegrityError
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.http import HttpResponse
from django.template.loader import render_to_string

from admin_user.models import Administrator
from bot.messages_texts.constants import (
    FAREWELL_TEACHER_MESSAGE, FAREWELL_STUDENT_MESSAGE,
)
from core.config.settings_base import EMAIL_HOST_USER
from potential_user.models import ApplicationForm
from schooling.models import Student, Teacher
from schooling.signals_bot import send_message_to_user
from django.contrib.auth import get_user_model


#TODO Перенести в сигналы bot_signals.py
@receiver(pre_delete, sender=Student)
@receiver(pre_delete, sender=Teacher)
async def delete_person_and_send_msg(sender, instance, *args, **kwargs):
    """Удалить и отправить выбранным пользователям прощальное сообщение."""
    await send_message_to_user(
        settings.TELEGRAM_TOKEN,
        instance.telegram_id,
        message_text=(
            FAREWELL_TEACHER_MESSAGE
            if instance.__class__.__name__ == 'Teacher'
            else FAREWELL_STUDENT_MESSAGE
        ),
    )


@receiver(post_save, sender=ApplicationForm)
def create_user_from_application(sender,
                                 instance: ApplicationForm,
                                 created,
                                 **kwargs):
    """Функция создания пользователя согласно роли в заявке."""
    if instance.approved:
        if instance.role == 'teacher':
            user = Teacher(telegram_id=instance.telegram_id,
                           name=instance.name,
                           surname=instance.surname,
                           city=instance.city,
                           phone_number=instance.phone_number, )
        elif instance.role == 'student':
            user = Student(telegram_id=instance.telegram_id,
                           name=instance.name,
                           surname=instance.surname,
                           city=instance.city,
                           phone_number=instance.phone_number,
                           study_class_id=instance.study_class_id,
                           parents_contacts=instance.parents_contacts, )
        try:
            user.save()
            instance.delete()
        except IntegrityError as err:
            raise ValueError(
                f'Пользователь с telegram_id {instance.telegram_id} '
                'уже существует.',
            ) from err


def send_registration_email(application_form):
    """Отправляет админу уведомление о новой заявке на регистрацию."""
    roles_mapping = {
        'student': 'Ученик',
        'teacher': 'Преподаватель',
    }

    subject = 'Goodstart: Новая заявка на регистрацию'
    user_role = roles_mapping.get(application_form.role, application_form.role)
    html_content = render_to_string(
        'mails/registration_notification_email.html',
        {
            'name': application_form.name,
            'surname': application_form.surname,
            'city': application_form.city,
            'phone_number': application_form.phone_number,
            'role': user_role,
        },
    )
    from_email = EMAIL_HOST_USER
    recipient_list = Administrator.objects.filter(
        is_active=True,
    ).values_list(
        'email',
        flat=True,
    )

    send_mail(
        subject,
        message=None,
        from_email=from_email,
        recipient_list=recipient_list,
        html_message=html_content,
    )
    return HttpResponse('Заявка на регистрацию принята!')


@sync_to_async
def send_feedback_email(subject, body, user, telegram_username=None):
    """Отправляет админу сообщение от зарегистрированного пользователя."""
    email_context = {
        'subject': f'{user.name} {user.surname}: {subject}',
        'body': body,
        'footer_meta_data_phone': (
            f'Телефон для связи: {user.phone_number}'
        ),
    }
    if telegram_username:
        email_context['footer_meta_data_tg_id'] = (
            f'Написать в telegram: https://t.me/{telegram_username}'
        )
    html_content = render_to_string(
        'mails/feedback_email.html',
        email_context,
    )
    from_email = EMAIL_HOST_USER
    recipient_list = Administrator.objects.filter(
        is_active=True,
    ).values_list(
        'email',
        flat=True,
    )

    send_mail(
        subject= f'Goodstart: {subject}',
        message=None,
        from_email=from_email,
        recipient_list=recipient_list,
        html_message=html_content,
    )


async def get_admin_emails():
    user_model = get_user_model()
    admins = await sync_to_async(user_model.objects.filter)(is_staff=True)
    return [admin.email for admin in await sync_to_async(list)(admins)]


async def send_cancel_lesson_email(lesson, user):
    from_email = EMAIL_HOST_USER
    recipient_list = Administrator.objects.filter(
        is_active=True,
    ).values_list(
        'email',
        flat=True,
    )
    moscow_tz = pytz.timezone('Europe/Moscow')
    new_datetime_moscow = lesson.datetime_start.astimezone(moscow_tz)
    formatted_datetime = new_datetime_moscow.strftime(
                '%Y-%m-%d %H:%M:%S',
            )
    email_context = {
        'subject': f'{user._meta.verbose_name} {user.name} {user.surname} запросил(а) отмену занятия', #Noqa
        'body': f'Название занятия - {lesson.name}. Дата и время - {formatted_datetime}', #Noqa
        'footer_meta_data_phone': (
            f'Телефон для связи: {user.phone_number}'
        ),
    }
    html_content = render_to_string(
        'mails/cansel_lesson_email.html',
        email_context,
    )
    await sync_to_async(send_mail)(
        subject='Goodstart: Запрос на отмену занятия.',
        message=None,
        from_email=from_email,
        recipient_list=recipient_list,
        html_message=html_content,
    )

async def send_change_lesson_email(lesson, user, formatted_datetime):
    from_email = EMAIL_HOST_USER
    recipient_list = Administrator.objects.filter(
        is_active=True,
    ).values_list(
        'email',
        flat=True,
    )
    email_context = {
        'subject': f'{user._meta.verbose_name} {user.name} {user.surname} запросил(а) перенос занятия', #Noqa
        'body': f'Название занятия - {lesson.name}. Новая дата и время - {formatted_datetime}', #Noqa
        'footer_meta_data_phone': (
            f'Телефон для связи: {user.phone_number}'
        ),
    }
    html_content = render_to_string(
        'mails/cansel_lesson_email.html',
        email_context,
    )
    await sync_to_async(send_mail)(
        subject='Goodstart: Запрос на перенос занятия.',
        message=None,
        from_email=from_email,
        recipient_list=recipient_list,
        html_message=html_content,
    )
