from babel.dates import format_datetime as form_date

def format_datetime(dt):
    """Функция для форматирования даты и времени в удобный формат."""
    date = form_date(dt, locale='ru')
    return date


def format_lesson_duration(start_time, end_time):
    """Функция для вычисления продолжительности занятия."""
    duration = (end_time - start_time).seconds // 60
    return f'{duration}'
