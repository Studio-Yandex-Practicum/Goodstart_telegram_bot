from datetime import datetime


def format_datetime(dt):
    """Функция для форматирования даты и времени в удобный формат."""

    return dt.strftime('%d %B, в %H.%M')


def format_lesson_duration(start_time, end_time):
    """Функция для вычисления продолжительности занятия."""

    duration = (end_time - start_time).seconds // 60
    return f'{duration}'
