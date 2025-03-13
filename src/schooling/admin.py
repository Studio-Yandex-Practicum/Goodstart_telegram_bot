from datetime import datetime

from django.contrib import admin, messages
from django.shortcuts import redirect
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.core.files.storage import default_storage
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group

from schooling.constants import LessonCategories, LESSON_MARKED_AS_PAST_MESSAGE
from schooling.models import (Student, Teacher, Subject, StudyClass,
                              Lesson, LessonGroup, HomeworkImage, HomeworkFile)
from schooling.forms import LessonForm, TeacherForm, HomeworkImageFormSet
from schooling.utils import pluralize_ru


admin.site.unregister(Group)


class HomeworkImageInline(admin.TabularInline):
    """Инлайн-форма для изображений в занятиях."""

    model = HomeworkImage
    formset = HomeworkImageFormSet
    extra = 2
    can_delete = True
    fields = ('image', 'image_preview',)
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        """Отображает превью изображения."""
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 150px;"/>',
                obj.image.url,
            )
        return 'Нет изображения'

    image_preview.short_description = 'Превью'


class HomeworkFileInline(admin.TabularInline):
    """Инлайн-форма для файлов (PDF, DOCX)."""

    model = HomeworkFile
    extra = 2


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    """Управление преподавателями."""

    form = TeacherForm
    list_display = ('name', 'surname', 'get_competences')
    icon_name = 'edit'
    search_fields = ('name', 'surname',)
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
    search_fields = ('name', 'surname',)
    icon_name = 'school'
    exclude = ('state',)

    def delete_view(self, request, object_id, extra_context=None):
        """Блокирует удаление студента с оплаченными занятиями."""
        obj = self.get_object(request, object_id)

        if request.method == 'POST':
            # Здесь проверяем оплаченные/активные занятия
            if obj and obj.paid_lessons > 0:
                self.message_user(
                    request,
                    'Нельзя удалить студента, '
                    'у которого остались оплаченные занятия. '
                    'Сначала используйте или удалите эти занятия!',
                    level=messages.ERROR,
                )
                # Возвращаемся к списку студентов, отменяя удаление
                return redirect('admin:schooling_student_changelist',)

        # Если занятий нет, вызываем стандартное удаление
        return super().delete_view(request, object_id, extra_context)

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
    search_fields = ('name', )
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
    inlines = [HomeworkImageInline, HomeworkFileInline]
    list_display = (
        'name', 'subject', 'teacher_id', 'student_id',
        'start_time', 'duration', 'is_passed',
        'regular_lesson',
    )
    list_filter = (
        'subject', 'teacher_id', 'student_id',
        'is_passed', DateListFilter,
    )
    autocomplete_fields = ('subject', 'teacher_id', 'student_id',)
    search_fields = (
        'student_id__name', 'student_id__surname',
        'teacher_id__name', 'teacher_id__surname',
        'name',
    )
    icon_name = 'access_time'
    actions = ['mark_as_passed']


    def save_formset(self, request, form, formset, change):
        """Сохранение формсета с поддержкой удаления изображений."""
        if formset.model == HomeworkImage:
            if not formset.is_valid():
                print('Ошибки валидации:', formset.errors)
                return

            # Удаляем изображения, отмеченные на удаление
            for deleted_form in formset.deleted_forms:
                obj = deleted_form.instance
                if obj.image and default_storage.exists(obj.image.name):
                    default_storage.delete(obj.image.name)
                obj.delete()

            # Сохраняем новые изображения
            instances = formset.save(commit=False)
            for obj in instances:
                obj.lesson = form.instance
                obj.save()

            formset.save()
        else:
            formset.save()

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
        'student','display_schedule', 'study_class_id', 'remaining_lessons',
        'parents_contacts',

    )
    inlines = [LessonInline]
    icon_name = 'Расписание'
    search_fields = ('student__name', 'student__surname',)
    ordering = ('created_at',)

    def has_add_permission(self, request, obj=None):
        """Запрещает добавление новых групп."""
        return False

    @admin.display(description='Класс')
    def study_class_id(self, obj):
        """Возвращает учебный класс ученика."""
        return obj.student.study_class_id

    @admin.display(description=mark_safe('Оплачено<br>занятий'))
    def remaining_lessons(self, obj):
        """Возвращает количество оставшихся оплаченных уроков."""
        return obj.student.paid_lessons

    @admin.display(description='Контакты родителей')
    def parents_contacts(self, obj):
        """Возвращает контакты родителей (более широкая колонка)."""
        return obj.student.parents_contacts

    @admin.display(description='Расписание')
    def display_schedule(self, obj):
        """Формирует расписание в виде таблицы."""
        days_of_week = {
            2: 'Понедельник',
            3: 'Вторник',
            4: 'Среда',
            5: 'Четверг',
            6: 'Пятница',
            7: 'Суббота',
            1: 'Воскресенье',
        }

        # Начало карточки с отступами
        schedule_html = ('<div style="margin: 5px 0; padding: 5px; border: '
                         '1px solid #ddd; border-radius: 8px;">')

        schedule_html += ('<table style="border: 1px solid #ddd; '
                          'border-collapse: collapse; width: 100%;">')
        schedule_html += '<thead style="background-color: #f8f9fa;">'
        schedule_html += '<tr>'
        schedule_html += ('<th style="border: 1px solid #ddd; padding: 8px; '
                          'text-align: center;">День</th>')
        schedule_html += ('<th style="border: 1px solid #ddd; padding: 8px; '
                          'text-align: center;">Дата</th>')
        schedule_html += ('<th style="border: 1px solid #ddd; padding: 8px; '
                          'text-align: center;">Время</th>')
        schedule_html += ('<th style="border: 1px solid #ddd; padding: 8px; '
                          'text-align: center;">Предмет</th>')
        schedule_html += ('<th style="border: 1px solid #ddd; padding: 8px; '
                          'text-align: center;">Преподаватель</th>')
        schedule_html += '</tr>'
        schedule_html += '</thead><tbody>'

        for day, day_name in days_of_week.items():
            lessons = obj.student.lessons.filter(
                datetime_start__week_day=day).order_by('datetime_start')

            if lessons.exists():
                for lesson in lessons:
                    date = lesson.datetime_start.strftime('%d.%m.%Y')
                    start_time = lesson.datetime_start.strftime('%H:%M')
                    end_time = lesson.datetime_end.strftime('%H:%M')
                    teacher = lesson.teacher_id
                    subject = lesson.subject

                    schedule_html += '<tr>'
                    schedule_html += (f'<td style="border: 1px solid #ddd; '
                                      f'padding: 8px;">{day_name}</td>')
                    schedule_html += (f'<td style="border: 1px solid #ddd; '
                                      f'padding: 8px; text-align: '
                                      f'center;">{date}</td>')
                    schedule_html += (f'<td style="border: 1px solid #ddd; '
                                      f'padding: 8px; text-align: center;'
                                      f'">{start_time} - {end_time}</td>')
                    schedule_html += (f'<td style="border: 1px solid #ddd; '
                                      f'padding: 8px;">{subject}</td>')
                    schedule_html += (f'<td style="border: 1px solid #ddd; '
                                      f'padding: 8px;">{teacher}</td>')
                    schedule_html += '</tr>'

        schedule_html += '</tbody></table>'
        schedule_html += '</div>'  # Закрываем div-контейнер
        return mark_safe(schedule_html)
