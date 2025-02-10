import os

from django.apps import AppConfig
from django_asgi_lifespan.signals import asgi_shutdown


class BotConfig(AppConfig):
    """"Configuration class for the bot application."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bot'

    def ready(self) -> None:
        """Perform bot start when the Django application is fully loaded."""
        if os.getenv('RUN_BOT', 'false').lower() == 'true':
            from bot.bot_interface import Bot

            self.bot = Bot()
            asgi_shutdown.connect(self.stop_bot)
            self.bot.start()

    def stop_bot(self, **kwargs):
        """Stop the bot if it was running."""
        self.bot.stop()
