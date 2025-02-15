from django.contrib import admin
from django.utils.safestring import mark_safe
import calendar

from schooling.models import (Student, Teacher, Subject, StudyClass,
                              Lesson, LessonGroup)
from schooling.forms import LessonForm


RU_MONTHS = {
    'January': 'Январь', 'February': 'Февраль', 'March': 'Март',
    'April': 'Апрель', 'May': 'Май', 'June': 'Июнь',
    'July': 'Июль', 'August': 'Август', 'September': 'Сентябрь',
    'October': 'Октябрь', 'November': 'Ноябрь', 'December': 'Декабрь',
}

RU_WEEKDAYS = {
    'Monday': 'Понедельник',
    'Tuesday': 'Вторник',
    'Wednesday': 'Среда',
    'Thursday': 'Четверг',
    'Friday': 'Пятница',
    'Saturday': 'Суббота',
    'Sunday': 'Воскресенье',
}

RU_WEEK_NAMES = [
    'Первая неделя', 'Вторая неделя', 'Третья неделя',
    'Четвертая неделя', 'Пятая неделя', 'Шестая неделя',
]


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
        'regular_lesson','lesson_count',
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
        'student', 'created_at', 'schedule',
        'paid_lessons', 'unpaid_lessons', 'current_lessons',
    )
    inlines = [LessonInline]
    icon_name = 'lesson_group'
    ordering = ('created_at',)

    def has_add_permission(self, request, obj=None):
        """Запрещает добавление новых групп."""
        return False

    @admin.display(description='Оплаченные занятия')
    def paid_lessons(self, obj):
        """Оплаченные занятия."""
        return obj.student.paid_lessons

    @admin.display(description='Неоплаченные занятия')
    def unpaid_lessons(self, obj):
        """Неоплаченные занятия."""
        unpaid_lessons = obj.lessons.all().count() - obj.student.paid_lessons
        if unpaid_lessons <= 0:
            return 0
        return unpaid_lessons

    @admin.display(description='Запланированные занятия')
    def current_lessons(self, obj):
        """Запланированные занятия."""
        return obj.lessons.all().count()

    @admin.display(description='Расписание')
    def schedule(self, obj):
        """Группированное расписание занятий по месяцам и неделям."""
        lessons = sorted(
            obj.lessons.all(), key=lambda lesson: lesson.datetime_start,
        )

        # Группировка по месяцам
        schedule_html = ''
        last_month = None
        last_week = None
        last_day = None
        for lesson in lessons:
            month = lesson.datetime_start.month
            week_number = (lesson.datetime_start.day - 1) // 7
            day_of_week = lesson.datetime_start.strftime('%A')
            day_label = f'{RU_WEEKDAYS[day_of_week]}'

            # Если месяц изменился, добавляем заголовок
            if month != last_month:
                year = lesson.datetime_start.strftime('%Y')
                month_name = (f'{RU_MONTHS.get(calendar.month_name[month])}, '
                              f'{year}')
                schedule_html += f'<h3>{month_name}</h3><br>'
                last_month = month
                last_week = None  # Сбрасываем неделю при смене месяца

            # Если неделя изменилась, добавляем заголовок недели
            if week_number != last_week:
                week_name = (
                    RU_WEEK_NAMES[week_number]
                    if week_number < len(RU_WEEK_NAMES)
                    else f'{week_number + 1}-я неделя'
                )
                schedule_html += f'<strong>{week_name}</strong><br>'
                last_week = week_number
                last_day = None  # Сбрасываем день при смене недели

            # Если день недели изменился, добавляем заголовок дня
            if day_label != last_day:
                schedule_html += (f'&nbsp;&nbsp;&nbsp;&nbsp;<strong>'
                                  f'{day_label}</strong><br>')
                last_day = day_label

            # Добавляем запись занятия
            date = lesson.datetime_start.strftime('%d.%m.%Y')
            start_time = lesson.datetime_start.strftime('%H:%M')
            end_time = lesson.datetime_end.strftime('%H:%M')
            schedule_html += (f'&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
                              f'{date} ({start_time} - {end_time}) '
                              f'- {lesson.subject}<br>')
        return mark_safe(schedule_html)
