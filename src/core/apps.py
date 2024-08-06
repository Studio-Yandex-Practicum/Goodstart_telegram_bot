from material.admin.apps import AdminConfig


class CustomAdminConfig(AdminConfig):
    """Оверрайд для добавления касмомизированного класса AdminSite."""

    default_site = 'core.admin.CustomAdminSite'
