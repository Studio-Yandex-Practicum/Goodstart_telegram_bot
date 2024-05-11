from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy

from .models import ApplicationForm
from .forms import RegistrationForm


class RegistrationCreateView(CreateView):

    model = ApplicationForm
    form_class = RegistrationForm
    template_name = 'registration/registration_form.html'

    # TODO убрать после реализации получения telegram_id
    def form_valid(self, form):
        form.instance.telegram_id = 12345678
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('registration:index')


# TODO убрать после реализации главной страницы
class TemplateIndex(ListView):
     model = ApplicationForm
     template_name = 'registration/fortest.html'
