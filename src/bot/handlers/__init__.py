from bot.handlers.echo import echo_handler
from bot.handlers.start import start_handler
from bot.handlers.success_registration import (
    success_registration_webapp_handler,
)
from bot.handlers.help import help_handler
from bot.handlers.feedback import feedback_handler
from bot.handlers.schedule import schedule_handler
from bot.handlers.was_the_lesson import lesson_end_handler
from bot.handlers.left_lessons import left_lessons_handler

__all__ = [
    'echo_handler', 'start_handler', 'help_handler',
    'success_registration_webapp_handler', 'feedback_handler',
    'schedule_handler', 'lesson_end_handler', 'left_lessons_handler',
]
