from django import forms

from .models import ApplicationForm


class RegistrationForm(forms.ModelForm):
    """Form to register a new user."""

    class Meta:
        """Form meta class."""
        model = ApplicationForm
        fields = {'name', 'surname', 'phone_number', 'city', }
