from django.contrib import admin
from django.utils.safestring import mark_safe
from django.shortcuts import render
from datetime import timedelta, datetime
import calendar

from django.urls import path

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

    # change_list_template = "admin/schedule_list.html"

    list_display = (
        'student', 'parents_contacts',
        'study_class_id', 'subjects', 'monday', 'tuesday',
        'wednesday', 'thursday', 'friday', 'saturday', 'sunday'
    )
    inlines = [LessonInline]
    icon_name = 'lesson_group'
    ordering = ('created_at',)

    class Media:
        css = {
            'all': ('styles/custom_admin.css',)  # Подключаем кастомный CSS
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

    @admin.display(description='Предмет')
    def subjects(self, obj):
        """Предмет."""
        schedule_html = ''
        subjects = [subject.name for subject in obj.student.subjects.all().order_by('name')]
        for subject in subjects:
            schedule_html += f'<strong>{subject}</strong><br>'
        return mark_safe(schedule_html)

    def weekday(self, obj, day):
        """Метод для отображения занятий по дням недели."""
        schedule_html = ''
        monday_lessons = obj.student.lessons.filter(datetime_start__week_day=day).order_by('datetime_start')
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

    # @admin.display(description='Преподаватель')
    # def study_class_id(self, obj):
    #     """Представитель и контакты."""
    #     return obj.lessons.all().count()

    # @admin.display(description='Оплаченные занятия')
    # def paid_lessons(self, obj):
    #     """Оплаченные занятия."""
    #     return obj.student.paid_lessons

    # @admin.display(description='Оплаченные занятия')
    # def paid_lessons(self, obj):
    #     """Оплаченные занятия."""
    #     return obj.student.paid_lessons

    # @admin.display(description='Неоплаченные занятия')
    # def unpaid_lessons(self, obj):
    #     """Неоплаченные занятия."""
    #     unpaid_lessons = obj.lessons.all().count() - obj.student.paid_lessons
    #     if unpaid_lessons <= 0:
    #         return 0
    #     return unpaid_lessons

    # @admin.display(description='Запланированные занятия')
    # def current_lessons(self, obj):
    #     """Запланированные занятия."""
    #     return obj.lessons.all().count()

    # @admin.display(description='Расписание')
    # def schedule(self, obj):
    #     """Группированное расписание занятий по месяцам и неделям."""
    #     lessons = sorted(
    #         obj.lessons.all(), key=lambda lesson: lesson.datetime_start,
    #     )

    #     # Группировка по месяцам
    #     schedule_html = ''
    #     last_month = None
    #     last_week = None
    #     last_day = None
    #     for lesson in lessons:
    #         month = lesson.datetime_start.month
    #         week_number = (lesson.datetime_start.day - 1) // 7
    #         day_of_week = lesson.datetime_start.strftime('%A')
    #         day_label = f'{RU_WEEKDAYS[day_of_week]}'

    #         # Если месяц изменился, добавляем заголовок
    #         if month != last_month:
    #             year = lesson.datetime_start.strftime('%Y')
    #             month_name = (f'{RU_MONTHS.get(calendar.month_name[month])}, '
    #                           f'{year}')
    #             schedule_html += f'<h3>{month_name}</h3><br>'
    #             last_month = month
    #             last_week = None  # Сбрасываем неделю при смене месяца

    #         # Если неделя изменилась, добавляем заголовок недели
    #         if week_number != last_week:
    #             week_name = (
    #                 RU_WEEK_NAMES[week_number]
    #                 if week_number < len(RU_WEEK_NAMES)
    #                 else f'{week_number + 1}-я неделя'
    #             )
    #             schedule_html += f'<strong>{week_name}</strong><br>'
    #             last_week = week_number
    #             last_day = None  # Сбрасываем день при смене недели

    #         # Если день недели изменился, добавляем заголовок дня
    #         if day_label != last_day:
    #             schedule_html += (f'&nbsp;&nbsp;&nbsp;&nbsp;<strong>'
    #                               f'{day_label}</strong><br>')
    #             last_day = day_label

    #         # Добавляем запись занятия
    #         date = lesson.datetime_start.strftime('%d.%m.%Y')
    #         start_time = lesson.datetime_start.strftime('%H:%M')
    #         end_time = lesson.datetime_end.strftime('%H:%M')
    #         schedule_html += (f'&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
    #                           f'{date} ({start_time} - {end_time}) '
    #                           f'- {lesson.subject}<br>')
    #     return mark_safe(schedule_html)
    
    # def get_urls(self):
    #     urls = super().get_urls()
    #     custom_urls = [
    #         path("", self.admin_site.admin_view(self.schedule_view), name="schedule"),
    #     ]
    #     return custom_urls + urls

    # def schedule_view(self, request):
    #     """Генерируем данные для таблицы"""
        # students = Student.objects.all()
        # parents_contacts = [student.parents_contacts for student in students]
        # student_lessons = {
        #     student.name: student.lessons.all() for student in students
        # }
        # today = datetime.today()
        # week_days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
        # time_slots = ["08:00-10:00", "10:00-12:00", "12:00-14:00", "14:00-16:00", "16:00-18:00"]

        # # Заполняем таблицу занятиями
        # schedule = {day: {slot: None for slot in time_slots} for day in week_days}
        # # lessons = Lesson.objects.filter(date__gte=today, date__lt=today + timedelta(days=7))
        # lessons = Lesson.objects.all()

        # for lesson in lessons:
        #     day_name = week_days[lesson.datetime_start.weekday()]
        #     schedule[day_name][time_slots[0]] = lesson

        # return render(request, "admin/schedule_list.html", {"schedule": schedule, "week_days": week_days, "time_slots": time_slots})
        # return render(
        #     request,
        #     'admin/schedule_list.html',
        #     {'week_days': week_days, 'students': students, 'parents_contacts': parents_contacts},

        # )
