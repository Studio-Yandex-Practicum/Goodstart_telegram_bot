from datetime import datetime

from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from schooling.constants import LessonCategories, LESSON_MARKED_AS_PAST_MESSAGE
from schooling.models import (Student, Teacher, Subject, StudyClass,
                              Lesson, LessonGroup)
from schooling.forms import LessonForm, TeacherForm
from schooling.utils import pluralize_ru


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    """Управление преподавателями."""

    form = TeacherForm
    list_display = ('name', 'surname', 'get_competences')
    icon_name = 'edit'
    exclude = ('state',)

    def has_add_permission(self, request, obj=None):
        """Запрещает добавление новых преподавателей."""
        return False

    @admin.display(description='Предмет')
    def get_competences(self, obj):
        """Возвращает компетенции преподавателя."""
        return '\n'.join([c.name for c in obj.competence.all()])


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    """Управление студентами."""

    list_display = (
        'name', 'surname', 'paid_lessons', 'unpaid_lessons',
        'current_lessons',
    )
    list_filter = (
        'name', 'surname', 'paid_lessons',
    )
    icon_name = 'school'
    exclude = ('state',)

    def has_add_permission(self, request, obj=None):
        """Запрещает добавление новых студентов."""
        return False

    @admin.display(description='Запланированные занятия')
    def current_lessons(self, obj):
        """Запланированные занятия."""
        return obj.lessons.all().count()

    @admin.display(description='Неоплаченные занятия')
    def unpaid_lessons(self, obj):
        """Неоплаченные занятия."""
        unpaid_lessons = obj.lessons.all().count() - obj.paid_lessons
        if unpaid_lessons <= 0:
            return 0
        return unpaid_lessons


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    """Управление школьными предметами."""

    list_display = ('name',)
    exclude = ('subject_key',)
    icon_name = 'subject'
    ordering = ('name',)


@admin.register(StudyClass)
class StudyClassAdmin(admin.ModelAdmin):
    """Управление учебными классами."""

    icon_name = 'groups'
    list_display = ('study_class_name', 'study_class_number',)
    list_filter = ('study_class_number',)


class DateListFilter(admin.SimpleListFilter):
    """Фильтр для выбора занятий по дате."""

    title = _('Дата занятия')
    parameter_name = 'lesson_date'

    def lookups(self, request, model_admin):
        """Возвращает список доступных дат для фильтрации."""
        dates = set(model_admin.get_queryset(
            request).values_list('datetime_start', flat=True))
        return [(date.strftime('%d-%m-%Y'),
                 date.strftime('%d-%m-%Y')) for date in dates if date]

    def queryset(self, request, queryset):
        """Фильтрует занятия по выбранной дате."""
        if self.value():
            try:
                date_obj = datetime.strptime(self.value(), '%d-%m-%Y')
                return queryset.filter(datetime_start__date=date_obj.date())
            except ValueError:
                return queryset.none()
        return queryset


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    """Управление занятиями."""

    form = LessonForm
    list_display = (
        'name', 'subject', 'teacher_id', 'student_id',
        'start_time', 'duration', 'is_passed',
        'regular_lesson',
    )
    list_filter = (
        'subject', 'teacher_id', 'student_id',
        'is_passed', DateListFilter,
    )
    search_fields = (
        'name', 'subject__name',
        'teacher_id__name', 'student_id__name',
    )
    icon_name = 'access_time'
    actions = ['mark_as_passed']

    @admin.display(description='Начало', ordering='datetime_start')
    def start_time(self, obj):
        """Обрабатывает поле datetime_start."""
        return obj.datetime_start

    @admin.action(description='Отметить выбранные занятия как прошедшие')
    def mark_as_passed(self, request, queryset):
        """Помечает выбранные занятия как прошедшие."""
        updated = queryset.update(is_passed=True)

        word = pluralize_ru(updated, ('занятие', 'занятия', 'занятий'))

        self.message_user(
            request,
            LESSON_MARKED_AS_PAST_MESSAGE.format(
                updated=updated,
                word=word,
                category=LessonCategories.IS_PASSED.value,
            ),
        )


class LessonInline(admin.StackedInline):
    """Для отображения занятий привязанных к студенту."""

    model = Lesson
    extra = 1  # Количество пустых форм для добавления новых записей
    fields = (
        'name', 'subject', 'student_id', 'teacher_id',
        'video_meeting_url', 'homework_url',
        'datetime_start', 'duration', 'regular_lesson', 'is_passed',
    )
    ordering = ('datetime_start',)


@admin.register(LessonGroup)
class LessonGroupAdmin(admin.ModelAdmin):
    """Управление группами занятий для студента."""

    list_display = (
        'student', 'parents_contacts',
        'study_class_id', 'monday', 'tuesday',
        'wednesday', 'thursday', 'friday', 'saturday', 'sunday',
    )
    inlines = [LessonInline]
    icon_name = 'lesson_group'
    ordering = ('created_at',)

    class Media:
        css = {
            'all': ('styles/custom_admin.css',),
        }

    def has_add_permission(self, request, obj=None):
        """Запрещает добавление новых групп."""
        return False

    @admin.display(description='Представитель / Контакт')
    def parents_contacts(self, obj):
        """Представитель и контакт."""
        return obj.student.parents_contacts

    @admin.display(description='Класс')
    def study_class_id(self, obj):
        """Класс."""
        return obj.student.study_class_id

    def weekday(self, obj, day):
        """Метод для отображения занятий по дням недели."""
        schedule_html = ''
        monday_lessons = obj.student.lessons.filter(
            datetime_start__week_day=day,
        ).order_by('datetime_start')
        for lesson in monday_lessons:
            teacher = lesson.teacher_id
            date = lesson.datetime_start.strftime('%d.%m.%Y')
            start_time = lesson.datetime_start.strftime('%H:%M')
            end_time = lesson.datetime_end.strftime('%H:%M')
            schedule_html += (f'&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
                              f'{date} '
                              f'(<strong>{start_time} - {end_time}) '
                              f'- {lesson.subject}</strong> ({teacher})<br>')
        return mark_safe(schedule_html)

    @admin.display(description='Понедельник')
    def monday(self, obj):
        """Возвращает список занятий, запланированных на понедельник."""
        return self.weekday(obj, 2)

    @admin.display(description='Вторник')
    def tuesday(self, obj):
        """Возвращает список занятий, запланированных на вторник."""
        return self.weekday(obj, 3)

    @admin.display(description='Среда')
    def wednesday(self, obj):
        """Возвращает список занятий, запланированных на среду."""
        return self.weekday(obj, 4)

    @admin.display(description='Четверг')
    def thursday(self, obj):
        """Возвращает список занятий, запланированных на четверг."""
        return self.weekday(obj, 5)

    @admin.display(description='Пятница')
    def friday(self, obj):
        """Возвращает список занятий, запланированных на пятницу."""
        return self.weekday(obj, 6)

    @admin.display(description='Суббота')
    def saturday(self, obj):
        """Возвращает список занятий, запланированных на субботу."""
        return self.weekday(obj, 7)

    @admin.display(description='Воскресенье')
    def sunday(self, obj):
        """Возвращает список занятий, запланированных на воскресенье."""
        return self.weekday(obj, 1)
