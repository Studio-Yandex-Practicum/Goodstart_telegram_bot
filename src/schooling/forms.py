from django import forms
from django.utils.translation import gettext_lazy as _

from schooling.models import Lesson

class LessonForm(forms.ModelForm):
    """Форма создания занятий"""

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

class ChangeDateTimeLesson(forms.Form):
    """Форма для запроса нового времени для урока."""

    dt_field = forms.DateTimeField(
        label='Новая дата и время занятия',
        widget=forms.DateTimeInput(
            attrs={'type': 'datetime-local'},
        ),
    )
