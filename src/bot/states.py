from django.db.models import TextChoices


class UserStates(TextChoices):
    """Класс, описывающий состояние пользователя при общении с ботом."""

    START = 'start'
    HELP = 'help'
    SCHEDULE = 'schedule'
    FEEDBACK = 'feedback'
    FEEDBACK_SUBJECT = 'feedback_subject_msg'
    FEEDBACK_BODY = 'feedback_body_msg'
    LEFT_LESSONS = 'left_lessons'
    WRITE_TEACHER = 'write_teacher'
    WRITE_TEACHER_MESSAGE = 'write_teacher_message'
    WRITE_STUDENT = 'write_student'
    WRITE_STUDENT_MESSAGE = 'write_student_message'
