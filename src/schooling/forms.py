from datetime import timedelta

from django import forms
from django.utils import timezone

from schooling.form_validators import (validate_intersections_time_periods,
                                       validate_paid_lessons,
                                       validate_teacher_subjects)
from schooling.models import Lesson


class LessonForm(forms.ModelForm):
    """Форма создания занятий."""

    class Meta:
        model = Lesson
        fields = (
            'name', 'subject', 'teacher_id', 'student_id',
            'datetime_start', 'duration', 'is_passed', 'test_lesson',
        )

    def clean(self):
        cleaned_data = super().clean()

        # Проверка наличия необходимых данных
        required_fields = ['datetime_start', 'duration',
                           'student_id', 'teacher_id',
                           'subject', 'test_lesson']
        for field in required_fields:
            if field not in cleaned_data:
                raise forms.ValidationError(
                    f'Поле {field} обязательно для заполнения.')

        datetime_start = cleaned_data.get('datetime_start')
        duration = cleaned_data.get('duration')
        student = cleaned_data.get('student_id')
        teacher = cleaned_data.get('teacher_id')
        subject = cleaned_data.get('subject')
        test_lesson = cleaned_data.get('test_lesson')

        # Валидация даты и времени начала урока
        if datetime_start:
            if datetime_start < timezone.now():
                raise forms.ValidationError(
                    'Дата и время начала урока должны быть в будущем.')
        else:
            raise forms.ValidationError(
                'Дата и время начала урока обязательны для заполнения.')

        # Валидация продолжительности урока
        if duration:
            if duration < 30 or duration > 180:
                raise forms.ValidationError(
                    'Длительность урока должна быть от 30 до 180 минут.')
        else:
            raise forms.ValidationError(
                'Продолжительность урока обязательна для заполнения.')

        # Валидация посещения студента
        if student:
            if not hasattr(student, 'last_login_date'):
                raise forms.ValidationError(
                    'У студента отсутствует информация о последнем посещении.')
            if student.last_login_date + timedelta(
                    days=60) < timezone.now().date():
                raise forms.ValidationError(
                    f'Студент не посещал занятия в '
                    f'течение последних двух месяцев.\n'
                    f'Последнее посещение: {student.last_login_date}.'
                )
        else:
            raise forms.ValidationError('Информация о студенте обязательна.')

        # Валидация посещения преподавателя
        if teacher:
            if not hasattr(teacher, 'last_login_date'):
                raise forms.ValidationError(
                    'У преподавателя отсутствует '
                    'информация о последнем посещении.')
            if teacher.last_login_date + timedelta(
                    days=60) < timezone.now().date():
                raise forms.ValidationError(
                    f'Преподаватель не проводил занятия в '
                    f'течение последних двух месяцев.\n'
                    f'Последнее посещение: {teacher.last_login_date}.'
                )
        else:
            raise forms.ValidationError(
                'Информация о преподавателе обязательна.')

        # Проведение остальных проверок
        try:
            validate_paid_lessons(student=student, test_lesson=test_lesson)
            validate_teacher_subjects(subject=subject, teacher=teacher)
            validate_intersections_time_periods(
                user=student,
                requested_time=datetime_start,
                requested_lesson_duration=duration,
                excluded_lesson=self.instance.id,
            )
            validate_intersections_time_periods(
                user=teacher,
                requested_time=datetime_start,
                requested_lesson_duration=duration,
                excluded_lesson=self.instance.id,
            )
        except Exception as e:
            raise forms.ValidationError(str(e))

        return cleaned_data


class ChangeDateTimeLesson(forms.Form):
    """Форма для запроса нового времени для урока."""

    dt_field = forms.DateTimeField(
        label='Новая дата и время занятия',
        widget=forms.DateTimeInput(
            attrs={'type': 'datetime-local'},
        ),
    )
