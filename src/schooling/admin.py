from django.contrib import admin

from schooling.models import Student, Teacher


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    """Управление преподавателями."""

    list_display = ('name', 'surname', 'competence')


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    """Управление студентами."""

    list_display = ('name', 'surname', 'paid_lessons')
