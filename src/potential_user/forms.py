from django import forms
from phonenumber_field.formfields import PhoneNumberField

from .models import ApplicationForm


class RegistrationForm(forms.ModelForm):

    class Meta:
        model = ApplicationForm
        fields = {'telegram_id', 'name', 'surname', 'phone_number', 'city', }

