import pytz

from babel.dates import format_datetime as form_date
from .constants import TIMEZONE_FOR_REMINDERS

def format_datetime(dt):
    """Функция для форматирования даты и времени в удобный формат."""
    tz = pytz.timezone(TIMEZONE_FOR_REMINDERS)  # Указываем нужный часовой пояс
    dt = dt.astimezone(tz)  # Преобразуем dt в UTC+3
    date = form_date(dt, locale='ru')
    return date

def format_time(dt):
    """Функция для форматирования времени в удобный формат без секунд."""
    tz = pytz.timezone(TIMEZONE_FOR_REMINDERS)  # Указываем нужный часовой пояс
    dt = dt.astimezone(tz)  # Преобразуем dt в UTC+3
    time = dt.strftime('%H:%M')  # Форматируем время без секунд
    return time


def format_lesson_duration(start_time, end_time):
    """Функция для вычисления продолжительности занятия."""
    duration = (end_time - start_time).seconds // 60
    return f'{duration}'


def pluralize_ru(number, word_forms):
    """
    Возвращает правильную форму слова для русского языка.

    :param number: Количество.
    :param word_forms: Кортеж из трёх форм слова.
    :return: Правильная форма слова.
    """
    if number % 10 == 1 and number % 100 != 11:
        return word_forms[0]
    elif 2 <= number % 10 <= 4 and (number % 100 < 10 or number % 100 >= 20):
        return word_forms[1]
    else:
        return word_forms[2]
