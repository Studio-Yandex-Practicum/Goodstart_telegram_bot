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
                Administrator.USERNAME_FIELD,
                *Administrator.REQUIRED_FIELDS,
                'password1',
                'password2',
                'is_staff',
                'is_superuser',
            ),
        }),
    )

    list_display = ('username', 'email',)
    search_fields = ('username', 'email',)
    list_filter = ('is_staff',)
    list_display_links = ('username',)
    search_help_text = 'Поиск по почте или имени пользователя.'
