# bot_interface.py
import asyncio
import threading
import time
from typing import Self

from django.conf import settings
from loguru import logger
from telegram import Update, BotCommand, MenuButtonCommands
from telegram.ext import (
    Application, ApplicationBuilder,
    CallbackQueryHandler, ConversationHandler,
    PersistenceInput, MessageHandler, filters,
)
from bot.handlers import (
    echo_handler, start_handler, help_handler, feedback_handler,
    success_registration_webapp_handler, schedule_handler,
    lesson_end_handler, left_lessons_handler,
)
from bot.handlers.feedback import subject, body
from bot.handlers.conversation import help, schedule
from bot.states import UserStates
from bot.persistence import DjangoPersistence
from bot.utils import add_daily_task

PERSISTENCE_UPDATE_DELAY = 5


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
        persistence = DjangoPersistence(
            PersistenceInput(
                bot_data=False,
                chat_data=False,
                user_data=False,
                callback_data=False,
            ),
            update_interval=PERSISTENCE_UPDATE_DELAY,
        )
        app = ApplicationBuilder().token(
            settings.TELEGRAM_TOKEN).persistence(persistence).build()
        main_handler = await build_main_handler()
        app.add_handlers([
            main_handler,
            start_handler,
            help_handler,
            success_registration_webapp_handler,
            echo_handler,
            feedback_handler,
            schedule_handler,
            lesson_end_handler,
            left_lessons_handler,
        ])
        await self._update_bot_commands(app)
        logger.info('Bot application built with handlers.')
        return app

    async def _update_bot_commands(self, app):
        """Update bot commands to be shown in the menu."""
        commands = [
            BotCommand('start', 'Запустить бот'),
            BotCommand('help', 'Помощь'),
            BotCommand('feedback', 'Отправить отзыв'),
            BotCommand('echo', 'Отправить эхо-сообщение'),
            BotCommand('schedule', 'Запланировать урок'),
            BotCommand('success_registration', 'Успешная регистрация'),
            BotCommand('left_lessons', 'Оставшиеся уроки'),
            BotCommand('was_the_lesson', 'Был ли урок'),
            # Сюда добавлять новые комманды
        ]
        await app.bot.set_my_commands(commands)
        await app.bot.set_chat_menu_button(chat_id=None, 
                                           menu_button=MenuButtonCommands())

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
        await add_daily_task()
        await self._app.updater.start_polling(allowed_updates=Update.ALL_TYPES)
        await self._app.start()
        logger.info('Bot is running.')
        while not self._stop_event.is_set():
            await asyncio.sleep(1)

        await self._app.stop()
        logger.info('Bot stopped.')

    async def get_app(self):
        """Public method to get the application instance."""
        if self._app is None:
            self._app = await self._build_app()
        return self._app


async def build_main_handler():
    """Функция создания главного обработчика."""
    return ConversationHandler(
        entry_points=[start_handler, feedback_handler],
        name='main_handler',
        persistent=True,
        states={
            UserStates.START: [
                feedback_handler,
                CallbackQueryHandler(help,
                                     pattern=f'^{UserStates.HELP.value}$'),
                CallbackQueryHandler(schedule,
                                     pattern=f'^{UserStates.SCHEDULE.value}$'),
            ],
            UserStates.HELP: [
                CallbackQueryHandler(
                    start_handler,
                    pattern=f'^{UserStates.START.value}$',
                ),
            ],
            UserStates.SCHEDULE: [
                CallbackQueryHandler(
                    start_handler,
                    pattern=f'^{UserStates.START.value}$',
                ),
            ],
            UserStates.LEFT_LESSONS: [
                CallbackQueryHandler(
                    left_lessons_handler,
                    pattern=f'^{UserStates.START.value}$',
                ),
            ],
            UserStates.FEEDBACK_SUBJECT: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    subject,
                ),
            ],
            UserStates.FEEDBACK_BODY: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    body,
                ),
            ],
        },
        fallbacks=[start_handler],
    )
