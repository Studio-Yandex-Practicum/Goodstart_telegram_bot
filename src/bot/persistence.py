from telegram.ext import BasePersistence
from asgiref.sync import sync_to_async
from django.db.utils import IntegrityError

from schooling.models import Teacher, Student
from bot.utils import check_user_from_db


class DjangoPersistence(BasePersistence):
    """Обрабатывает состояния пользователей."""

    def _get_all_users(self):
        """Вспомогательный метод для получения всех пользователей."""
        teachers = Teacher.objects.all()
        students = Student.objects.all()
        return list(teachers) + list(students)

    async def get_conversations(self, name):
        """Получение состояний пользователей."""
        conversations = {}
        users = await sync_to_async(self._get_all_users)()
        for user in users:
            conversations[user.telegram_id] = user.state
        return {name: conversations}

    async def update_conversation(self, name, key, new_state) -> None:
        """
        Обновление поля state в объекте пользователя.

        Python-telegram-bot по умолчанию хранит два параметра
        в кортеже key: user_id и chat_id. Goodstart использует только
        telegram_id, поэтому в кортеже хранятся два одинаковых id.
        """
        user = await check_user_from_db(
            telegram_id=key[0],
            from_models=[Teacher, Student],
        )
        if user:
            try:
                user.state = new_state
                await user.asave()
            except IntegrityError as error:
                print(f'Возникла ошибка при сохранении состояния: {error}')

    async def get_bot_data(self):
        """Заглушка для неиспользуемого метода."""
        ... # noqa

    async def update_bot_data(self):
        """Заглушка для неиспользуемого метода."""
        ... # noqa

    async def refresh_bot_data(self):
        """Заглушка для неиспользуемого метода."""
        ... # noqa

    async def get_chat_data(self):
        """Заглушка для неиспользуемого метода."""
        ... # noqa

    async def update_chat_data(self):
        """Заглушка для неиспользуемого метода."""
        ... # noqa

    async def refresh_chat_data(self):
        """Заглушка для неиспользуемого метода."""
        ... # noqa

    async def drop_chat_data(self):
        """Заглушка для неиспользуемого метода."""
        ... # noqa

    async def get_user_data(self):
        """Заглушка для неиспользуемого метода."""
        ... # noqa

    async def update_user_data(self):
        """Заглушка для неиспользуемого метода."""
        ... # noqa

    async def refresh_user_data(self):
        """Заглушка для неиспользуемого метода."""
        ... # noqa

    async def drop_user_data(self):
        """Заглушка для неиспользуемого метода."""
        ... # noqa

    async def get_callback_data(self):
        """Заглушка для неиспользуемого метода."""
        ... # noqa

    async def update_callback_data(self):
        """Заглушка для неиспользуемого метода."""
        ... # noqa

    async def flush(self):
        """Заглушка для неиспользуемого метода."""
        ... # noqa
