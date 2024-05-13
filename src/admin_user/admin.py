from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from admin_user.models import Administrator


@admin.register(Administrator)
class AdministratorAdmin(UserAdmin):
    """Admin panel for the Admin model in the Django admin area."""

    fieldsets = (
        (
            None,
            {
                'fields': (
                    'email',
                    'password',
                ),
            },
        ),
        (
            'Личная информация', {
                'fields': (
                    'first_name',
                    'last_name',
                    'phone',
                ),
            },
        ),
        (
            'Разрешения', {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                ),
            },
        ),
        (
            'История активности', {
                'fields': (
                    'last_login',
                    'date_joined',
                ),
            },
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'email',
                    'first_name',
                    'last_name',
                    'password1',
                    'password2',
                    'is_staff',
                    'is_superuser',
                ),
            },
        ),
    )

    list_display = ('email',)
    search_fields = ('email',)
    list_filter = ('is_staff',)
    search_help_text = 'Поиск по почте или имени пользователя.'
    ordering = ('last_name',)
