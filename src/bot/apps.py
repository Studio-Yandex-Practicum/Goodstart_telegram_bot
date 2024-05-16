import os
import sys
import signal

from django.apps import AppConfig


class BotConfig(AppConfig):
    """Configuration class for the bot application."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bot'

    def ready(self) -> None:
        """Perform bot start when the Django application is fully loaded."""
        if os.environ.get('RUN_MAIN', None) == 'true':
            self._start_bot()

        signal.signal(signal.SIGINT, self._handle_sigint)

    def _start_bot(self):
        """Initialize and start the Telegram bot."""
        from bot.bot_interface import Bot

        self.bot = Bot()
        self.bot.start()

    def _stop_bot(self, **kwargs):
        """Stop the bot if it was running."""
        if hasattr(self, 'bot') and hasattr(self.bot, 'stop'):
            self.bot.stop()

    def _handle_sigint(self, signum, frame):
        """
        Handle interrupt signal (Ctrl+C).

        Method is called when an interrupt signal (Ctrl+C) is received.
        It stops the bot and exits the application gracefully.
        """
        self._stop_bot()
        sys.exit(0)
