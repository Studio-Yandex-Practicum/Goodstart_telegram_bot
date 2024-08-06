from datetime import date, datetime, timedelta
from typing import Union

from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from schooling.models import Lesson, Student, Teacher


def validate_intersections_time_periods(
    user: Union[Teacher, Student],
    requested_time: datetime,
    requested_lesson_duration: int,
    excluded_lesson: Union[None, int],
) -> None:
    """
    Проверка в форме создаваемого занятия.

    Проверяет пересечения по времени с существующим.
    """
    if not all([user, requested_time, requested_lesson_duration]):
        raise forms.ValidationError('Отсутствуют необходимые данные.')
    if isinstance(user, Teacher):
        user_lessons_queryset = Lesson.objects.filter(
            teacher_id=user,
            datetime_start__date=date(
                requested_time.year,
                requested_time.month,
                requested_time.day,
            ),
        ).exclude(pk=excluded_lesson)
    elif isinstance(user, Student):
        user_lessons_queryset = Lesson.objects.filter(
            student_id=user,
            datetime_start__date=date(
                requested_time.year,
                requested_time.month,
                requested_time.day,
            ),
        ).exclude(pk=excluded_lesson)

    for scheduled_lesson in user_lessons_queryset:
        potential_lesson_time_start = scheduled_lesson.datetime_start
        potential_lesson_duration = scheduled_lesson.duration
        requested_end_time = (
            requested_time + timedelta(minutes=requested_lesson_duration)
        )
        potential_end_time = (
            potential_lesson_time_start + timedelta(
                minutes=potential_lesson_duration,
            )
        )
        duration_1 = requested_end_time - requested_time
        duration_2 = potential_end_time - potential_lesson_time_start
        total_duration = max(requested_end_time, potential_end_time) - min(
            requested_time, potential_lesson_time_start,
        )
        if total_duration < (duration_1 + duration_2):
            raise forms.ValidationError(
                {
                    'datetime_start': _(
                        'Время занятия пересекается c другим!',
                    ),
                },
            )


def validate_paid_lessons(student: Student, test_lesson: bool) -> None:
    lessons_count = Lesson.objects.filter(
        student_id=student,
        test_lesson=False,
        is_passed=False,
    ).count()
    if not test_lesson:
        if lessons_count >= student.paid_lessons:
            raise forms.ValidationError(
                {'student_id': _('Исчерпан лимит оплаченных занятий!')},
            )


def validate_teacher_subjects(subject: str, teacher: Teacher) -> None:
    if subject not in teacher.competence.all():
        raise forms.ValidationError(
            {'subject': _('Предмет преподаёт другой преподаватель!')},
        )


def validate_lesson_datetime(datetime_start):
    """Валидация даты и времени начала урока."""
    if datetime_start < timezone.now():
        raise ValidationError(
            'Дата и время начала урока должны быть в будущем.')


def validate_lesson_duration(duration):
    """Валидация продолжительности урока."""
    if duration < 30 or duration > 180:
        raise ValidationError(
            'Длительность урока должна быть от 30 до 180 минут.')


def validate_student_last_login(student):
    """Валидация посещения студента."""
    if not hasattr(student, 'last_login_date'):
        raise ValidationError(
            'У студента отсутствует информация о последнем посещении.')
    if student.last_login_date + timedelta(days=180) < timezone.now().date():
        raise ValidationError(
            f'Студент не посещал занятия в течение последних шести месяцев.\n'
            f'Последнее посещение: {student.last_login_date}.',
        )


def validate_teacher_last_login(teacher):
    """Валидация посещения преподавателя."""
    if not hasattr(teacher, 'last_login_date'):
        raise ValidationError(
            'У преподавателя отсутствует информация о последнем посещении.')
    if teacher.last_login_date + timedelta(days=60) < timezone.now().date():
        raise ValidationError(
            f'Преподаватель не проводил занятия '
            f'в течение последних двух месяцев.\n'
            f'Последнее посещение: {teacher.last_login_date}.',
        )
