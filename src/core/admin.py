from django.contrib.admin import AdminSite


class GoodStartAdminSite(AdminSite):
    """Кастомный класс сайта администрирования."""

    site_header = 'GoodStart школа'
    index_title = 'Администрирование'

admin_site = GoodStartAdminSite()
