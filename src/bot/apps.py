from django.apps import AppConfig
from django_asgi_lifespan.signals import asgi_shutdown


class BotConfig(AppConfig):
    """Configuration class for the bot application."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "bot"

    def stop_bot(self, **kwargs):
        self.bot.stop()

    def ready(self) -> None:
        """Perform actions when the application is ready."""
        import os

        if os.environ.get('RUN_MAIN', None) != 'true':
            from bot.bot_interface import Bot

            self.bot = Bot()

            asgi_shutdown.connect(self.stop_bot)

            self.bot.start()