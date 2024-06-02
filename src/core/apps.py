from django.contrib.admin.apps import AdminConfig


class GoodStartAdminConfig(AdminConfig):
    default_site = 'core.admin.GoodStartAdminSite'
