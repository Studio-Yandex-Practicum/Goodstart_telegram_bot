from django.contrib.admin.apps import AdminConfig


class GoodStartAdminConfig(AdminConfig):
    """Переопределение сайта администратора по умолчанию."""

    default_site = 'core.admin.GoodStartAdminSite'
