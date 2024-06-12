from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.http import HttpResponse
from django.template.loader import render_to_string

from admin_user.models import Administrator
from bot.messages_texts.constants import (
    FAREWELL_TEACHER_MESSAGE, FAREWELL_STUDENT_MESSAGE,
)
from core.config.settings_base import EMAIL_HOST_USER
from schooling.models import Student, Teacher
from schooling.utils import send_message_to_user


@receiver(pre_delete, sender=Student)
@receiver(pre_delete, sender=Teacher)
def delete_person_and_send_msg(sender, instance, *args, **kwargs):
    """Удалить и отправить выбранным пользователям прощальное сообщение."""
    send_message_to_user(
        settings.TELEGRAM_TOKEN,
        instance.telegram_id,
        message_text=(
            FAREWELL_TEACHER_MESSAGE
            if instance.__class__.__name__ == 'Teacher'
            else FAREWELL_STUDENT_MESSAGE
        ),
    )


def send_registration_email(application_form):
    """Отправляет админу уведомление о новой заявке на регистрацию."""
    roles_mapping = {
        'student': 'Ученик',
        'teacher': 'Преподаватель',
    }

    subject = 'Goodstart: Новая заявка на регистрацию'
    user_role = roles_mapping.get(application_form.role, application_form.role)
    html_content = render_to_string(
        'emailing/registration_notification_email.html',
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
