from django.contrib import admin

from potential_user.models import ApplicationForm


@admin.register(ApplicationForm)
class ApplicationFormAdmin(admin.ModelAdmin):
    """Управление заявками."""

    icon_name = 'priority_high'
