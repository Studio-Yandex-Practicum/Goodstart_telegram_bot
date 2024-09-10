from django.apps import AppConfig


class SchoolingConfig(AppConfig):
    """Config of schooling app for interactions with learning entities."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'schooling'
    verbose_name = 'Обучение в школе'

    def ready(self) -> None:
        """Подлючает сигналы."""
        from schooling import signals_bot # noqa
