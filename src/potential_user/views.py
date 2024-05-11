from django.views.generic import CreateView

from .models import ApplicationForm
from .forms import RegistrationForm


class RegistrationCreateView(CreateView):

    model = ApplicationForm
    form_class = RegistrationForm
    template_name = 'registration/registration_form.html'
