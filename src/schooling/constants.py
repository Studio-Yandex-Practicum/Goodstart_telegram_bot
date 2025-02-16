from enum import Enum


class LessonCategories(str, Enum):
    """Перечисление категорий уроков."""

    IS_PASSED = 'прошедшие'


LESSON_MARKED_AS_PAST_MESSAGE = (
    'Вы поместили {updated} {word} в категорию "{category}".'
)
LONG_TIME_REMINDER=60
SHORT_TIME_REMINDER=5
TIMEZONE_FOR_REMINDERS='Europe/Moscow'
