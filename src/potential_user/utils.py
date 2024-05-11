import random
import sys

from .models import ApplicationForm


def get_telegram_id() -> int:
    """
    Получает телеграм id от бота.

    Сейчас исполняет роль заглушки.
    """
    while True:
        telegram_id = random.randint(0, sys.maxsize)
        tg_id_in_db = ApplicationForm.objects.filter(
            telegram_id=telegram_id,
        ).exists()
        if tg_id_in_db:
            continue
        return telegram_id
