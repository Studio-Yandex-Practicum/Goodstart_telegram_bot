import asyncio
import threading
import time
from typing import Self

from django.conf import settings
from loguru import logger
from telegram import Update
from telegram.ext import (Application, ApplicationBuilder,
                          CallbackQueryHandler, ConversationHandler,
                          PicklePersistence)

from bot.handlers import echo_handler, start_handler
from bot.handlers.conversation import help, schedule
from bot.states import States



class Bot:
    """A singleton-class representing a Telegram bot."""

    _instance: Self | None = None

    def __new__(cls, *args, **kwargs):
        """Singleton constructor. Only one instance of Bot is created."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize the bot. Ensures initialization happens only once."""
        if not hasattr(self, 'initialized'):
            self.initialized = True
            self._app: Application | None = None
            self._stop_event = asyncio.Event()
            logger.info('Bot instance created.')

    def start(self):
        """Start the bot in a separate thread and sets up signal handling."""
        logger.info('Bot starting...')
        self._stop_event.clear()
        bot_thread = threading.Thread(target=self._run)
        bot_thread.start()
        logger.info('Bot started in a new thread.')

    def stop(self):
        """Stop the bot."""
        logger.info('Bot stopping...')
        self._stop_event.set()
        time.sleep(1)

    async def _build_app(self):
        """Build the application."""
        persistence = PicklePersistence(filepath=settings.PERSISTENCE_PATH)
        app = ApplicationBuilder().token(
            settings.TELEGRAM_TOKEN).persistence(
                persistence).build()
        main_handler = await build_main_handler()
        app.add_handlers([
            main_handler,
            start_handler,
            echo_handler,
            ])

        logger.info('Bot application built with handlers.')
        return app

    def _run(self):
        """Run the bot."""
        asyncio.set_event_loop(asyncio.new_event_loop())
        logger.info('Bot event loop created and started.')
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(self._start_bot())
        finally:
            loop.close()
            logger.info('Bot event loop closed.')

    async def _start_bot(self):
        """Start the bot."""
        self._app = await self._build_app()
        await self._app.initialize()
        await self._app.updater.start_polling(allowed_updates=Update.ALL_TYPES)
        await self._app.start()
        logger.info('Bot is running.')
        while not self._stop_event.is_set():
            await asyncio.sleep(1)

        await self._app.stop()
        logger.info('Bot stopped.')


async def build_main_handler():
    """Функция создания главного обработчика."""
    return ConversationHandler(
        entry_points=[start_handler],
        persistent=True,
        name="main_handler",
        states={
            States.START: [
                CallbackQueryHandler(help,
                                     pattern=f'^{States.HELP.value}$'),
                CallbackQueryHandler(schedule,
                                     pattern=f'^{States.SCHEDULE.value}$'),
            ],
        },
        fallbacks=[start_handler],
        )
