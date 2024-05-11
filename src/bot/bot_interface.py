import asyncio
import threading

from django.conf import settings
from telegram.ext import ApplicationBuilder

from bot.handlers import echo_handler, start_handler


class Bot:
    """A class representing a Telegram bot."""

    def __init__(self):
        """Initialize the bot."""
        self._app: None
        self._stop_event = threading.Event()

    def start(self):
        """Start the bot in a separate thread and sets up signal handling."""
        self._stop_event.clear()
        bot_thread = threading.Thread(target=self._run)
        bot_thread.start()

    def stop(self):
        """Stop the bot."""
        self._stop_event.set()

    async def _build_app(self):
        """Build the application."""
        app = ApplicationBuilder().token(settings.TELEGRAM_TOKEN).build()
        app.add_handler(start_handler)
        app.add_handler(echo_handler)
        return app

    def _run(self):
        """Run the bot."""
        asyncio.set_event_loop(asyncio.new_event_loop())
        asyncio.get_event_loop().run_until_complete(self._start_bot())

    async def _start_bot(self):
        """Start the bot."""
        self._app = await self._build_app()
        await self._app.initialize()
        await self._app.updater.start_polling()
        await self._app.start()
        while not self._stop_event.is_set():
            await asyncio.sleep(1)

        await self._app.stop()
