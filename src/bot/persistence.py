from telegram.ext import BasePersistence
from asgiref.sync import sync_to_async

from schooling.models import Teacher, Student


class DjangoPersistence(BasePersistence):
    """Обрабатывает состояния пользователей."""

    def _get_all_users(self):
        """Вспомогательный метод для получения всех пользователей."""
        teachers = Teacher.objects.all()
        students = Student.objects.all()
        return list(teachers) + list(students)
    
    async def get_conversations(self, name):
        conversations = {}
        users = await sync_to_async(self._get_all_users)()
        for user in users:
            conversations[user.telegram_id] = user.state
        return {name: conversations}
    
    async def get_bot_data(self):
        """Заглушка для неиспользуемого метода."""
        pass

    async def update_bot_data(self):
        """Заглушка для неиспользуемого метода."""
        pass

    async def refresh_bot_data(self):
        """Заглушка для неиспользуемого метода."""
        pass

    async def get_chat_data(self):
        """Заглушка для неиспользуемого метода."""
        pass

    async def update_chat_data(self):
        """Заглушка для неиспользуемого метода."""
        pass

    async def refresh_chat_data(self):
        """Заглушка для неиспользуемого метода."""
        pass

    async def drop_chat_data(self):
        """Заглушка для неиспользуемого метода."""
        pass

    async def get_user_data(self):
        """Заглушка для неиспользуемого метода."""
        pass

    async def update_user_data(self):
        """Заглушка для неиспользуемого метода."""
        pass

    async def refresh_user_data(self):
        """Заглушка для неиспользуемого метода."""
        pass

    async def drop_user_data(self):
        """Заглушка для неиспользуемого метода."""
        pass

    async def get_callback_data(self):
        """Заглушка для неиспользуемого метода."""
        pass

    async def update_callback_data(self):
        """Заглушка для неиспользуемого метода."""
        pass

    async def update_conversation(self):
        """Заглушка для неиспользуемого метода."""
        pass

    async def flush(self):
        """Заглушка для неиспользуемого метода."""
        pass

