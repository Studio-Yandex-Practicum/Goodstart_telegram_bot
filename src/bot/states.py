from django.db.models import TextChoices


class UserStates(TextChoices):
    """Класс, описывающий состояние пользователя при общении с ботом."""

    START = 'start'
    HELP = 'help'
    SCHEDULE = 'schedule'
