from django.core.mail import send_mail
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.db import IntegrityError
from django.db.models.signals import post_save
from django.dispatch import receiver

from admin_user.models import Administrator
from core.config.settings_base import EMAIL_HOST_USER
from schooling.models import Student, Teacher
from potential_user.models import ApplicationForm


@receiver(post_save, sender=ApplicationForm)
def create_user_from_application(sender, instance, created, **kwargs):
    """Функция создания пользователя согласно роли в заявке."""
    if instance.approved:
        if instance.role == 'teacher':
            user_model = Teacher
        elif instance.role == 'student':
            user_model = Student
        try:
            user_model.objects.create(
                telegram_id=instance.telegram_id,
                name=instance.name,
                surname=instance.surname,
                city=instance.city,
                phone_number=instance.phone_number,
                # study_class_id=StudyClass.objects.get(id=1),
                # parents_contacts='null',
            )
            instance.delete()
        except IntegrityError as err:
            raise ValueError(
                f'Пользователь с telegram_id {instance.telegram_id} '
                'уже существует.',
            ) from err
    # TODO: Возможно обработать сценарий, если пользователь существует.


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
