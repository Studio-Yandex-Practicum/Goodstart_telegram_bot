from django.apps import AppConfig


class PotentialUserConfig(AppConfig):
    """Config of PotentialUserApp."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'potential_user'
    verbose_name = 'Заявки на регистрацию'
