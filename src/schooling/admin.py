from django.contrib import admin
from django.utils.safestring import mark_safe
from itertools import groupby
import calendar

from schooling.models import (Student, Teacher, Subject, StudyClass,
                              Lesson, LessonGroup)
from schooling.forms import LessonForm


RU_MONTHS = {
    'January': 'Январь', 'February': 'Февраль', 'March': 'Март',
    'April': 'Апрель', 'May': 'Май', 'June': 'Июнь',
    'July': 'Июль', 'August': 'Август', 'September': 'Сентябрь',
    'October': 'Октябрь', 'November': 'Ноябрь', 'December': 'Декабрь'
}

RU_WEEKDAYS = {
    'Monday': 'Понедельник',
    'Tuesday': 'Вторник',
    'Wednesday': 'Среда',
    'Thursday': 'Четверг',
    'Friday': 'Пятница',
    'Saturday': 'Суббота',
    'Sunday': 'Воскресенье'
}


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

    list_display = ('name', 'surname', 'paid_lessons')
    icon_name = 'school'
    exclude = ('state',)

    def has_add_permission(self, request, obj=None):
        """Запрещает добавление новых студентов."""
        return False


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
        'start_time', 'duration', 'is_passed', 'test_lesson',
        'lesson_count'
    )
    list_filter = (
        'subject', 'teacher_id', 'student_id',
        'datetime_start', 'is_passed', 'test_lesson',
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
    model = Lesson
    extra = 1  # Количество пустых форм для добавления новых записей
    fields = (
        'name', 'subject', 'teacher_id',
        'video_meeting_url', 'homework_url',
        'datetime_start', 'duration', 'is_passed'
    )
    ordering = ('datetime_start',)


@admin.register(LessonGroup)
class LessonGroupAdmin(admin.ModelAdmin):
    """Управление группами занятий для студента."""

    list_display = (
        'student', 'created_at', 'schedule',
    )
    inlines = [LessonInline]
    icon_name = 'lesson_group'
    ordering = ('created_at',)

    def has_add_permission(self, request, obj=None):
        """Запрещает добавление новых групп."""
        return False
    
    @admin.display(description='Расписание')
    def schedule(self, obj):
        """Группированное расписание занятий по месяцам и дням недели."""
        pattern_date = '%d.%m.%Y %H:%M'
        
        # Получаем все занятия, отсортированные по дате
        lessons = sorted(
            obj.lessons.all(),
            key=lambda l: (l.datetime_start.month,
                           l.datetime_start.weekday(),
                           l.datetime_start))
        
        # Группировка по месяцам
        schedule_html = ''
        for month, month_lessons in groupby(
            lessons, key=lambda l: l.datetime_start.month
        ):
            schedule_html += (f'<strong>'
                              f'{RU_MONTHS.get(calendar.month_name[month])}'
                              f'</strong><br>')
            
            # Группировка по дням недели
            for day, day_lessons in groupby(
                month_lessons,
                key=lambda l: l.datetime_start.strftime('%A, %d')
            ):
                day = day.split(', ')
                schedule_html += (f'&nbsp;&nbsp;<em>'
                                  f'{RU_WEEKDAYS.get(day[0])}, '
                                  f'{day[1]}</em><br>')
                for lesson in day_lessons:
                    time_str = lesson.datetime_start.strftime('%H:%M')
                    schedule_html += (f'&nbsp;&nbsp;&nbsp;&nbsp;{time_str}'
                                     f' - {lesson.subject}<br>')
        return mark_safe(schedule_html)
