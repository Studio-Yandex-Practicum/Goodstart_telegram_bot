from django import forms

from schooling.models import Lesson
from schooling.validators.form_validators import (
    validate_intersections_time_periods,
    validate_lesson_duration, validate_paid_lessons,
    validate_student_last_login, validate_teacher_last_login,
    validate_teacher_subjects)


class LessonForm(forms.ModelForm):
    """Форма создания занятий."""

    class Meta:
        model = Lesson
        fields = (
            'name',
            'subject',
            'teacher_id',
            'student_id',
            'video_meeting_url',
            'homework_url',
            'datetime_start',
            'duration',
            'is_passed',
            'test_lesson',
            'lesson_count',
        )

    def clean(self):
        """
        Выполняет валидацию и очистку данных формы.

        Вызывает:
            forms.ValidationError: Если какое-либо обязательное поле
            отсутствует или валидация не проходит.

        Возвращает:
            dict: Очищенные и провалидированные данные.
        """
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
        if not datetime_start:
            raise forms.ValidationError(
                'Дата и время начала урока обязательны для заполнения.')

        # Валидация продолжительности урока
        if duration:
            validate_lesson_duration(duration)
        else:
            raise forms.ValidationError(
                'Продолжительность урока обязательна для заполнения.')

        # Валидация посещения студента
        if student:
            validate_student_last_login(student)
        else:
            raise forms.ValidationError('Информация о студенте обязательна.')

        # Валидация посещения преподавателя
        if teacher:
            validate_teacher_last_login(teacher)
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
            raise forms.ValidationError(str(e)) from e

        return cleaned_data


class ChangeDateTimeLesson(forms.Form):
    """Форма для запроса нового времени для урока."""

    dt_field = forms.DateTimeField(
        label='Новая дата и время занятия',
        widget=forms.DateTimeInput(
            attrs={'type': 'datetime-local'},
        ),
    )
