from collections.abc import Callable, Sequence
from typing import Any

from django.contrib import admin
from django.http import HttpRequest

from potential_user.models import ApplicationForm


@admin.register(ApplicationForm)
class ApplicationFormAdmin(admin.ModelAdmin):
    """Управление Заявками."""

    icon_name = 'priority_high'
    actions = ['approve_applications']

    def get_fields(self,
                   request: HttpRequest,
                   obj: ApplicationForm) -> Sequence[Callable[..., Any] | str]:
        """Для роли Учителя возращает не все поля."""
        if obj and obj.role == 'teacher':
            return ['telegram_id',
                    'role',
                    'name',
                    'surname',
                    'city',
                    'phone_number',
                    'approved']
        fields = super().get_fields(request, obj)
        return fields

    @admin.action(description='Подтвердить выбранные заявки')
    def approve_applications(self, request, queryset):
        """Перевести все выбранные заявки в статус 'Подтверждено'."""
        for query in queryset:
            query.approved = True
            query.save()
