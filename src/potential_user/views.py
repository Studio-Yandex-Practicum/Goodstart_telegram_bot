from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from .forms import RegistrationForm
from .models import ApplicationForm
from .utils import get_telegram_id


class RegistrationCreateView(CreateView):
    """Создает форму регистрации нового пользователя."""

    model = ApplicationForm
    form_class = RegistrationForm
    template_name = 'registration/registration_form.html'

    # TODO убрать после реализации получения telegram_id
    def form_valid(self, form):
        """Присваивает telegram_id."""
        form.instance.telegram_id = get_telegram_id()
        return super().form_valid(form)

    def get_success_url(self):
        """Переадресовывет на главную страницу."""
        return reverse_lazy('registration:index')


# TODO убрать после реализации главной страницы
class TemplateIndex(ListView):
    """Временная вьюха для регистрации."""

    model = ApplicationForm
    template_name = 'registration/fortest.html'
