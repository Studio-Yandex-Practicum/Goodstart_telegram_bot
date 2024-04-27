import logging
import sys

from django.core.management.base import BaseCommand
from django.conf import settings
from telegram.error import Forbidden
from telegram.ext import ApplicationBuilder

from bot.handlers import start_handler, echo_handler

class Command(BaseCommand):
    help = 'Телеграм-бот'

    def handle(self, *args, **kwargs):
        try:
            pass
        except Forbidden:
            logging.error("Invalid TELEGRAM_TOKEN.")
            sys.exit(1)

        bot = ApplicationBuilder().token(settings.TELEGRAM_TOKEN).build()
        bot.add_handler(start_handler)
        bot.add_handler(echo_handler)
        bot.run_polling()
