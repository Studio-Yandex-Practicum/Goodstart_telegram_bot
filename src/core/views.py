from admin_user.models import Administrator
from django.core.mail import send_mail
from django.http import HttpResponse
from django.template.loader import render_to_string

from core.config.settings_base import EMAIL_HOST_USER


# TODO: убрать после реализации функционала
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
