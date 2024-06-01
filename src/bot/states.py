from enum import Enum


class States(str, Enum):
    """Класс, описывающий состояния бота."""

    START = 'start'
    HELP = 'help'
    SCHEDULE = 'schedule'
