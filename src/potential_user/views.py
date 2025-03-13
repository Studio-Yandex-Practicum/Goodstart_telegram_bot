from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.shortcuts import render, redirect
from django.contrib import messages
from loguru import logger
from django.contrib.auth import get_user_model

from potential_user.forms import RegistrationForm
from potential_user.models import ApplicationForm
from core.logging import log_errors
from core.utils import send_registration_email


class RegistrationCreateView(CreateView):
    """Создает форму регистрации нового пользователя."""

    model = ApplicationForm
    form_class = RegistrationForm
    template_name = 'registration_form.html'

    @log_errors
    def form_valid(self, form):
        """Присваивает telegram_id и проверяет дубликаты."""
        telegram_id = self.kwargs.get('id')

        # Проверка, существует ли уже заявка от этого telegram_id
        if ApplicationForm.objects.filter(telegram_id=telegram_id).exists():
            messages.warning(self.request,
                             '📌 Вы уже подали заявку на регистрацию.')
            return redirect(self.get_success_url())

        form.instance.telegram_id = telegram_id
        response = super().form_valid(form)
        try:
            send_registration_email(self.object)
        except OSError as e:
            logger.error(f'Ошибка отправки письма: {e}')
             # Получаем email администратора
            admin_email = get_user_model().objects.filter(
                is_superuser=True,
            ).values_list('email', flat=True).first()

            if admin_email:
                messages.error(
                    self.request,
                    (f'⚠ Не удалось отправить письмо. Пожалуйста, свяжитесь'
                     f'с администратором: {admin_email}'),
                )
        return response

    def get_success_url(self):
        """Переадресовывет на страницу успешной регистрации."""
        return reverse_lazy('registration:registration_success')


def registration_success(request):
    return render(request, 'registration_success.html')
