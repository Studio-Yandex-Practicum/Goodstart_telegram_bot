from django.db.models import TextChoices


class UserStates(TextChoices):
    """Класс, описывающий состояние пользователя при общении с ботом."""

    START = 'start'
    HELP = 'help'
    SCHEDULE = 'schedule'
    FEEDBACK = 'feedback'
    FEEDBACK_SUBJECT_MSG = 'feedback_subject_msg'
    FEEDBACK_BODY_MSG = 'feedback_body_msg'
