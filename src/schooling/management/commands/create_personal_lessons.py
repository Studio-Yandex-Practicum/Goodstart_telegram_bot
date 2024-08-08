from django.core.management.base import BaseCommand
from schooling.factories.factories import LessonFactory


class Command(BaseCommand):
    """Команда для создания уроков для ученика по его Telegram ID."""

    help = 'Создание уроков для ученика по его Telegram ID'

    def add_arguments(self, parser):
        """Добавление аргументов команды."""
        parser.add_argument(
            '--telegram_id',
            type=int,
            required=True,
            help='Telegram ID ученика',
        )

    def handle(self, *args, **options):
        """Создание уроков для ученика по его Telegram ID."""
        telegram_id = options['telegram_id']
        LessonFactory.create_personal_lessons(telegram_id)
        self.stdout.write(
            self.style.SUCCESS(
                f'Успешно созданы уроки для ученика {telegram_id}'),)
