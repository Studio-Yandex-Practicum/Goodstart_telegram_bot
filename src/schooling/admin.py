from django.contrib import admin
from django.conf import settings

from .utils import send_message_to_user
from bot.messages_texts.constants import FAREWELL_TEACHER_MESSAGE
from schooling.models import Student, Teacher, Subject, StudyClass, Lesson


class CustomModelAdmin(admin.ModelAdmin):
    actions = ['delete_and_send_message']

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    @admin.action(description='Удалить и отправить сообщение')
    def delete_and_send_message(self, request, queryset):
        for query in queryset:
            send_message_to_user(
                settings.TELEGRAM_TOKEN,
                query.telegram_id,
                message_text=FAREWELL_TEACHER_MESSAGE
            )
            query.delete()


@admin.register(Teacher)
class TeacherAdmin(CustomModelAdmin):
    """Управление преподавателями."""

    list_display = ('name', 'surname', 'get_competences')
    icon_name = 'edit'

    @admin.display(description='Предмет')
    def get_competences(self, obj):
        """Return competences."""
        return '\n'.join([c.name for c in obj.competence.all()])

    @admin.action(description='Подтвердить выбранные заявки')
    def approve_applications(self, request, queryset):
        for query in queryset:
            query.approved = True
            query.save()


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    """Управление студентами."""

    list_display = ('name', 'surname', 'paid_lessons')
    icon_name = 'school'


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

    list_display = (
        'name', 'subject', 'teacher_id', 'student_id',
        'datetime_start', 'datetime_end', 'is_passed', 'test_lesson',
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
