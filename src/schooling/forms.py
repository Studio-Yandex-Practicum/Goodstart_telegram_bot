from django import forms


class ChangeDateTimeLesson(forms.Form):
    """Форма для запроса нового времени для урока."""

    dt_field = forms.DateTimeField(
        label='Новая дата и время занятия',
        widget=forms.DateTimeInput(
            attrs={'type': 'datetime-local'},
        ),
    )
