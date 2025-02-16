from django.contrib import admin
from django.utils.safestring import mark_safe

from schooling.models import (Student, Teacher, Subject, StudyClass,
                              Lesson, LessonGroup)
from schooling.forms import LessonForm


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    """Управление преподавателями."""

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
        'datetime_start', 'is_passed',
    )
    search_fields = (
        'name', 'subject__name',
        'teacher_id__name', 'student_id__name',
    )
    icon_name = 'access_time'

    @admin.display(description='Начало', ordering='datetime_start')
    def start_time(self, obj):
        """Обрабатывает поле datetime_start."""
        return obj.datetime_start


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

    # @admin.display(description='Предмет')
    # def subjects(self, obj):
    #     """Предмет."""
    #     schedule_html = ''
    #     subjects = [
    #         subject.name for subject in
    #         obj.student.subjects.all().order_by('name')
    #     ]
    #     for subject in subjects:
    #         schedule_html += f'<strong>{subject}</strong><br>'
    #     return mark_safe(schedule_html)

    # @admin.display(description='Преподаватель')
    # def teachers(self, obj):
    #     """Предмет."""
    #     schedule_html = ''
    #     lessons = [
    #         lesson for lesson in
    #         obj.student.su.all().order_by('datetime_start')
    #     ]
    #     for lesson in lessons:
    #         schedule_html += f'<strong>{lesson.teacher_id}</strong><br>'
    #     return mark_safe(schedule_html)

    def weekday(self, obj, day):
        """Метод для отображения занятий по дням недели."""
        schedule_html = ''
        monday_lessons = obj.student.lessons.filter(
            datetime_start__week_day=day,
        ).order_by('datetime_start')
        for lesson in monday_lessons:
            date = lesson.datetime_start.strftime('%d.%m.%Y')
            start_time = lesson.datetime_start.strftime('%H:%M')
            end_time = lesson.datetime_end.strftime('%H:%M')
            schedule_html += (f'&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
                              f'{date} ({start_time} - {end_time}) '
                              f'- {lesson.subject}<br>')
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
