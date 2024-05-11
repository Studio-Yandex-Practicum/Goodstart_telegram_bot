from django import forms

from .models import ApplicationForm


class RegistrationForm(forms.ModelForm):

    class Meta:
        model = ApplicationForm
        fields = {'name', 'surname', 'phone_number', 'city', }
