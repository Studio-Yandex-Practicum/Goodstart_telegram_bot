from datetime import date, timedelta

from django import forms
from django.utils.translation import gettext_lazy as _

from schooling.models import Lesson


def validation_intersections_time_periods(
    list_periods,
    start_1,
    time_1,
):
    """Проверка входит новый период занятия к остаольным."""
    for scheduled_lesson in list_periods:
        start_2 = scheduled_lesson.datetime_start
        time_2 = scheduled_lesson.duration
        end_1 = (start_1 + timedelta(minutes=time_1))
        end_2 = (start_2 + timedelta(minutes=time_2))
        duration_1 = end_1 - start_1
        duration_2 = end_2 - start_2
        total_duration = max(end_1, end_2) - min(start_1, start_2)
        if total_duration < (duration_1 + duration_2):
            raise forms.ValidationError(
                {'start_time': ('Период пересекается'), },
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
        student = self.cleaned_data['student_id']
        test_lesson = self.cleaned_data['test_lesson']
        teacher = self.cleaned_data['teacher_id']
        subject = self.cleaned_data['subject']
        datetime_start = self.cleaned_data['datetime_start']
        duration = self.cleaned_data['duration']

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
        if subject not in teacher.competence.all():
            raise forms.ValidationError(
                {'subject': _('Предмет преподаёт другой преподаватель!')},
            )

        student_lessons = Lesson.objects.filter(
            student_id=student,
            datetime_start__date=date(
                datetime_start.year,
                datetime_start.month,
                datetime_start.day,
                ),
        )
        validation_intersections_time_periods(
            student_lessons, datetime_start, duration,
        )
        teacher_lessons = Lesson.objects.filter(
            teacher_id=teacher,
            datetime_start__date=date(
                datetime_start.year,
                datetime_start.month,
                datetime_start.day,
                ),
        )
        validation_intersections_time_periods(
            teacher_lessons, datetime_start, duration,
        )


class ChangeDateTimeLesson(forms.Form):
    """Форма для запроса нового времени для урока."""

    dt_field = forms.DateTimeField(
        label='Новая дата и время занятия',
        widget=forms.DateTimeInput(
            attrs={'type': 'datetime-local'},
        ),
    )
