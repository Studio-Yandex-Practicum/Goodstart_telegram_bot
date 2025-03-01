from django.conf import settings
from django.urls import reverse
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

from asgiref.sync import sync_to_async
from schooling.models import Student

async def get_root_markup(telegram_id):
    try:
        user = await sync_to_async(
            Student.objects.get)(telegram_id=telegram_id)
        paid_lessons = user.paid_lessons
    except Student.DoesNotExist:
        paid_lessons = 0

    schedule_url = f"{settings.BASE_URL}{reverse(
        'schedule:schedule',
        kwargs={'id': telegram_id}
    )}"
    keyboard = [
        [
            InlineKeyboardButton(
                text='📜 Посмотреть расписание',
                web_app=WebAppInfo(url=schedule_url),
            ),
        ],
    ]
    if paid_lessons < 2:
        keyboard.append([
            InlineKeyboardButton(
                text='Оплатить занятия',
                web_app=WebAppInfo(
                    url=f'{settings.BASE_URL}/page43174319.html#price'),
            ),
        ])
    return InlineKeyboardMarkup(keyboard)
