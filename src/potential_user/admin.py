from django.contrib import admin

from potential_user.models import ApplicationForm


@admin.register(ApplicationForm)
class ApplicationFormAdmin(admin.ModelAdmin):
    """Управление заявками."""

    icon_name = 'priority_high'
    actions = ['approve_applications']

    @admin.action(description='Подтвердить выбранные заявки')
    def approve_applications(self, request, queryset):
        for query in queryset:
            query.approved = True
            query.save()
