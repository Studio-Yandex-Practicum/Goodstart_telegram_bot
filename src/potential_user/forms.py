from django import forms

from potential_user.models import ApplicationForm


class RegistrationForm(forms.ModelForm):
    """Form to register a new user."""

    class Meta:
        """Form meta class."""

        model = ApplicationForm
        fields = {'name', 'role', 'surname', 'phone_number', 'city', }
