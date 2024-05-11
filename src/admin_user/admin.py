from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from admin_user.models import Administrator


@admin.register(Administrator)
class AdministratorAdmin(UserAdmin):
    """
    Admin panel for the Admin model in the Django admin area.

    Changes made:
    - 'USERNAME_FIELD from the User model is used for creating a user.'

    Search is available by email or username.
    """

    add_fieldsets = (
        (None, {
            'fields': (
                *Administrator.REQUIRED_FIELDS,
                Administrator.USERNAME_FIELD,
                'password1',
                'password2',
                'is_staff',
                'is_superuser',
            ),
        }),
    )

    list_display = ('email',)
    search_fields = ('email',)
    list_filter = ('is_staff',)
    search_help_text = 'Поиск по почте или имени пользователя.'
    ordering = ('last_name',)
