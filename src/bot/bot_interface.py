# bot_interface.py
import asyncio
import threading
import time
from typing import Self

from asgiref.sync import sync_to_async
from django.conf import settings
from loguru import logger
from telegram import (BotCommand, BotCommandScopeChat, MenuButtonCommands,
                      Update)
from telegram.ext import (Application, ApplicationBuilder,
                          CallbackQueryHandler, ConversationHandler,
                          MessageHandler, PersistenceInput, filters)

from bot.handlers import (feedback_handler, help_handler, left_lessons_handler,
                          lesson_end_handler, schedule_handler, start_handler,
                          success_registration_webapp_handler,
                          unknown_command_handler)
from bot.handlers.conversation import help
from bot.handlers.feedback import body, subject
from bot.persistence import DjangoPersistence
from bot.states import UserStates
from bot.utils import add_daily_task
from schooling.models import Student, Teacher

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
            unknown_command_handler,
            feedback_handler,
            schedule_handler,
            lesson_end_handler,
            left_lessons_handler,
        ])
        await app.bot.delete_my_commands()
        await self._update_bot_commands(app)
        logger.info('Bot application built with handlers.')
        return app

    async def _update_bot_commands(self, app):
        """Обновление команд меню бота."""
        unregistered_commands = [
            BotCommand('start', 'Запустить бота'),
            BotCommand('help', 'Необходима регистрация'),
        ]

        teacher_commands = [
            BotCommand('start', 'Запустить бота'),
            BotCommand('schedule', 'Просмотреть расписание'),
            BotCommand('feedback', 'Отправить отзыв'),
            BotCommand('help', 'Все доступные команды бота'),
        ]

        student_commands = teacher_commands + [
            BotCommand('left_lessons', 'Оставшиеся уроки'),
        ]

        async def set_commands_for_users(users, commands):
            for user in users:
                try:
                    # Попробуем установить команды для пользователя
                    await app.bot.set_my_commands(
                        commands, scope=BotCommandScopeChat(
                            chat_id=user.telegram_id))
                    await app.bot.set_chat_menu_button(
                        chat_id=user.telegram_id,
                        menu_button=MenuButtonCommands())
                except Exception as e:
                    if 'Chat not found' in str(e):
                        logger.warning(
                            f'Пропуск пользователя '
                            f'{user.telegram_id}: Чат не найден')
                    else:
                        logger.error(
                            f'Ошибка при установке команд для '
                            f'пользователя {user.telegram_id}: {e}')

        try:
            await app.bot.delete_my_commands()
            await app.bot.set_my_commands(unregistered_commands)
            await app.bot.set_chat_menu_button(
                chat_id=None, menu_button=MenuButtonCommands())

            teachers = await sync_to_async(list)(Teacher.objects.all())
            students = await sync_to_async(list)(Student.objects.all())

            await set_commands_for_users(teachers, teacher_commands)
            await set_commands_for_users(students, student_commands)

            logger.info('Команды бота успешно обновлены для всех ролей.')

        except Exception as e:
            logger.error(f'Ошибка при обновлении команд бота: {e}')

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

        # Запуск периодического обновления команд
        asyncio.create_task(self._periodic_update_bot_commands())

        while not self._stop_event.is_set():
            await asyncio.sleep(1)

        await self._app.stop()
        logger.info('Bot stopped.')

    async def _periodic_update_bot_commands(self):
        """Периодически обновлять команды бота."""
        while not self._stop_event.is_set():
            await self._update_bot_commands(self._app)
            await asyncio.sleep(180)  # Обновлять команды каждые 30 минут

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
                start_handler,
                CallbackQueryHandler(help,
                                     pattern=f'^{UserStates.HELP.value}$'),
                CallbackQueryHandler(schedule_handler,
                                     pattern=f'^{UserStates.SCHEDULE.value}$'),
            ],
            UserStates.HELP: [
                CallbackQueryHandler(
                    help_handler,
                    pattern=f'^{UserStates.HELP.value}$',
                ),
            ],
            UserStates.SCHEDULE: [
                CallbackQueryHandler(
                    schedule_handler,
                    pattern=f'^{UserStates.SCHEDULE.value}$',
                ),
            ],
            UserStates.LEFT_LESSONS: [
                CallbackQueryHandler(
                    left_lessons_handler,
                    pattern=f'^{UserStates.LEFT_LESSONS.value}$',
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
