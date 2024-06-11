from bot.handlers.echo import echo_handler
from bot.handlers.start import start_handler
from bot.handlers.success_registration import (
    success_registration_webapp_handler,
)
from bot.handlers.help import help_handler
from bot.handlers.schedule import schedule_handler

__all__ = [
    'echo_handler', 'start_handler', 'help_handler',
    'success_registration_webapp_handler', 'schedule_handler',
]
