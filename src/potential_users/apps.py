from django.apps import AppConfig


class PotentialUsersConfig(AppConfig):
    """Config of PotentialUsersApp."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "potential_users"
    verbose_name = "Заявки на регистрацию"
