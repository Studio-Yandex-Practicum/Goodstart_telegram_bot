from django.apps import AppConfig


class AdminUserConfig(AppConfig):
    """Django config for admin_user app."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'admin_user'
    verbose_name = 'Управление администраторами'
