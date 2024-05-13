from django.contrib import admin

from .models import StudyClass


@admin.register(StudyClass)
class StudyClassAdmin(admin.ModelAdmin):
    """Управление учебными классами."""

    list_display = ('study_class_name', 'study_class_number')
