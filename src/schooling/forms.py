from django import forms

from schooling.models import Lesson
from schooling.form_validators import (
    validate_intersections_time_periods,
    validate_paid_lessons,
    validate_teacher_subjects,
    checking_for_lesson_updates,
)


class LessonForm(forms.ModelForm):
    """Форма создания занятий."""

    class Meta:
        model = Lesson
        fields = (
            'name', 'subject', 'teacher_id', 'student_id',
            'datetime_start', 'duration', 'is_passed', 'test_lesson',
        )

    def clean(self):
        """Валидация полей student_id и Subject модели Lesson."""
        super().clean()
        name = self.cleaned_data['name']
        student = self.cleaned_data['student_id']
        test_lesson = self.cleaned_data['test_lesson']
        teacher = self.cleaned_data['teacher_id']
        subject = self.cleaned_data['subject']
        datetime_start = self.cleaned_data['datetime_start']
        duration = self.cleaned_data['duration']

        validate_paid_lessons(student=student, test_lesson=test_lesson)
        validate_teacher_subjects(subject=subject, teacher=teacher,)
        excluded_lesson = checking_for_lesson_updates(
            name, subject, teacher, student, datetime_start,
        )
        validate_intersections_time_periods(
            user=student,
            requested_time=datetime_start,
            requested_lesson_duration=duration,
            excluded_lesson=excluded_lesson,
        )
        validate_intersections_time_periods(
            user=teacher,
            requested_time=datetime_start,
            requested_lesson_duration=duration,
            excluded_lesson=excluded_lesson,
        )


class ChangeDateTimeLesson(forms.Form):
    """Форма для запроса нового времени для урока."""

    dt_field = forms.DateTimeField(
        label='Новая дата и время занятия',
        widget=forms.DateTimeInput(
            attrs={'type': 'datetime-local'},
        ),
    )
