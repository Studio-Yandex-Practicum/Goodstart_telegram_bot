from collections.abc import Callable, Sequence
from typing import Any

from django.contrib import admin
from django.http import HttpRequest

from potential_user.models import ApplicationForm
from potential_user.constants import APPROVE_VALIDATION_TEXT


@admin.register(ApplicationForm)
class ApplicationFormAdmin(admin.ModelAdmin):
    """Управление Заявками."""

    icon_name = 'priority_high'
    actions = ['approve_applications']

    def has_add_permission(self, request):
        """Запрет на создание новых заявок из админки."""
        return False

    def get_fields(self,
                   request: HttpRequest,
                   obj: ApplicationForm) -> Sequence[Callable[..., Any] | str]:
        """
        Прячет поле telegram_id.

        Для роли Учителя возвращает не весь набор полей.
        """
        if obj and obj.role == 'teacher':
            return ['role',
                    'name',
                    'surname',
                    'city',
                    'phone_number',
                    'approved']
        fields = super().get_fields(request, obj)
        fields.remove('telegram_id')
        return fields

    @admin.action(description='Подтвердить выбранные заявки')
    def approve_applications(self, request, queryset):
        """Перевести все выбранные заявки в статус 'Подтверждено'."""
        application: bool = False
        for query in queryset:
            if (
                query.role == 'student' and
                query.study_class_id is None and
                query.parents_contacts is None
            ):
                application = True
            else:
                query.approved = True
                query.save()
        if application:
            self.message_user(request, APPROVE_VALIDATION_TEXT)
