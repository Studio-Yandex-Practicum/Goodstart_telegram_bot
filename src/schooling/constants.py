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

DEFAULT_TRIAL_LESSON_BROADCAST_TEXT = (
    '''Летние каникулы близятся к концу, скоро начнется учебный год 📚 Команда преподавателей Goodstart уже трудится во всю и проводит уроки 🥰

Наши лучшие репетиторы проводят пробные занятия и забивают свое расписание на учебное время! Чтобы не опоздать к хорошему преподавателю, рекомендуем заранее записаться, пройти бесплатный урок и зафиксировать свое расписание, оплатив удобный формат занятий 📅

Записаться на пробный урок 👇'''
)
