from django.db.models import TextChoices


class UserStates(TextChoices):
    """Класс, описывающий состояние пользователя при общении с ботом."""

    START = 'start'
    HELP = 'help'
    SCHEDULE = 'schedule'
    FEEDBACK = 'feedback'
    FEEDBACK_SUBJECT = 'feedback_subject_msg'
    FEEDBACK_BODY = 'feedback_body_msg'
