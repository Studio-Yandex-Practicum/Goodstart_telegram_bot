from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.shortcuts import render

from potential_user.forms import RegistrationForm
from potential_user.models import ApplicationForm


class RegistrationCreateView(CreateView):
    """Создает форму регистрации нового пользователя."""

    model = ApplicationForm
    form_class = RegistrationForm
    template_name = 'registration/registration_form.html'

    # TODO убрать после реализации получения telegram_id
    def form_valid(self, form):
        """Присваивает telegram_id."""
        form.instance.telegram_id = self.kwargs.get('id')
        return super().form_valid(form)

    def get_success_url(self):
        """Переадресовывет на страницу успешной регистрации."""
        return reverse_lazy('registration:registration_success')


def registration_success(request):
    return render(request, 'registration/registration_success.html')
