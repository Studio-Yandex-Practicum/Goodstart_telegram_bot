from django import forms
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory

from schooling.models import (
    Lesson, Teacher, HomeworkImage,
    MAX_COUNT_CLASSES, MAX_COUNT_SUBJECTS)
from schooling.validators.form_validators import (
    validate_intersections_time_periods,
    validate_lesson_duration, validate_paid_lessons,
    validate_student_last_login, validate_teacher_last_login,
    validate_teacher_subjects)


class MultipleFileInput(forms.ClearableFileInput):
    """Виджет для выбора нескольких файлов."""

    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    """Поле формы для загрузки нескольких файлов."""

    widget = MultipleFileInput

    def clean(self, data, initial=None):
        """Очистка данных, поддерживающая списки файлов."""
        if isinstance(data, (list, tuple)):
            return [super().clean(d, initial) for d in data]
        return super().clean(data, initial)


class HomeworkForm(forms.ModelForm):
    """Форма редактирования домашнего задания."""

    homework_text = forms.CharField(
        label='Текст домашнего задания',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 8}),
        required=False,
    )
    images = MultipleFileField(
        label='Добавить изображения',
        required=False,
    )
    files = MultipleFileField(
        label='Прикрепить файлы (PDF, DOCX и др.)',
        required=False,
    )

    class Meta:
        model = Lesson
        fields = ['homework_text']


class HomeworkImageForm(forms.ModelForm):
    """Форма для загрузки изображений домашнего задания."""

    class Meta:
        model = HomeworkImage
        fields = ('image', )


HomeworkImageFormSet = inlineformset_factory(
    Lesson,
    HomeworkImage,
    form=HomeworkImageForm,
    extra=2,
    can_delete=True,
)


class TeacherForm(forms.ModelForm):
    """Форма для валидации ManyToMany в админке."""

    class Meta:
        model = Teacher
        fields = (
            'telegram_id',
            'name',
            'surname',
            'city',
            'phone_number',
            'state',
            'competence',
            'study_classes',
        )
    def clean_competence(self):
        """Проверка количества предметов."""
        competence = self.cleaned_data['competence']
        if len(competence) > MAX_COUNT_SUBJECTS:
            raise ValidationError(
                f'Преподаватель не может вести более '
                f'{MAX_COUNT_SUBJECTS} предметов!')
        return competence

    def clean_study_classes(self):
        """Проверка количества классов."""
        study_classes = self.cleaned_data['study_classes']
        if len(study_classes) > MAX_COUNT_CLASSES:
            raise ValidationError(
                f'Преподаватель не может вести более '
                f'{MAX_COUNT_CLASSES} классов!')
        return study_classes


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
            'homework_text',
            'datetime_start',
            'duration',
            'regular_lesson',
            'is_passed',
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
                           'subject',]
        for field in required_fields:
            if field not in cleaned_data:
                raise forms.ValidationError(
                    f'Поле {field} обязательно для заполнения.')

        datetime_start = cleaned_data.get('datetime_start')
        duration = cleaned_data.get('duration')
        student = cleaned_data.get('student_id')
        teacher = cleaned_data.get('teacher_id')
        subject = cleaned_data.get('subject')
        regular_lesson = cleaned_data.get('regular_lesson')

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
            if not regular_lesson:
                validate_paid_lessons(student=student)
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
