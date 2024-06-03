from asgiref.sync import async_to_sync
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from telegram import Bot

from bot.keyboards import get_root_markup
from schooling.models import Student, Teacher


@async_to_sync
async def send_message_to_user(bot_token, user_id,
                               message_text,
                               reply_markup=None):
    """Инициативно отправляет сообщение."""
    bot = Bot(token=bot_token)
    await bot.send_message(chat_id=user_id,
                           text=message_text,
                           reply_markup=reply_markup)


@receiver(post_save, sender=Teacher)
@receiver(post_save, sender=Student)
def start_chat(sender, instance, created, **kwargs):
    """Отправляет уведомление об одобрении заявки."""
    if created:
        reply_markup = async_to_sync(get_root_markup)()
        send_message_to_user(settings.TELEGRAM_TOKEN,
                             instance.telegram_id,
                             message_text='Ваша заявка одобрена!',
                             reply_markup=reply_markup)
