from django.core.mail import send_mail
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from .config.settings_base import EMAIL_HOST_USER, DEFAULT_RECEIVER
from admin_user.models import Administrator


# TODO: убрать после реализации функционала
def send_greeting_email(request):
    """
    Тестовая функция для проверки отправки email.

    Использует предварительно заданный DEFAULT_RECEIVER
    из переменных окружения для определения получателя.
    Проверяет существование пользователя с таким email в базе данных.
    Отправляет приветственное письмо
    с использованием шаблона 'emailing/greeting_email.html'.

    """
    user_email = DEFAULT_RECEIVER
    if not user_email:
        return HttpResponse(
            'Email не задан в переменных окружения.',
            status=400,
        )
    user_exists = Administrator.objects.filter(email=user_email).exists()
    if not user_exists:
        return HttpResponse(
            'Сначала зарегистрируйте пользователя с данным email.',
            status=404,
        )

    user = Administrator.objects.get(email=user_email)

    subject = 'Привет!'
    convert_to_html_content = render_to_string(
        'emailing/greeting_email.html',
        {'user': user.first_name},
    )
    message = strip_tags(convert_to_html_content)
    from_email = EMAIL_HOST_USER
    recipient_list = [user.email]

    send_mail(subject, message, from_email, recipient_list)
    return HttpResponse('Email отправлен!')
