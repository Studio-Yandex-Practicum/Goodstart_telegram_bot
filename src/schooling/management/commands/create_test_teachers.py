from django.core.management.base import BaseCommand

from schooling.factories import create_teachers


class Command(BaseCommand):
    """Command to Teacher instances creation for the project tests."""

    def _generate(self):
        create_teachers()

    def handle(self, *args, **options):
        """Call the method `_generate` for the test Teacher creation."""
        self._generate()
        return self.stdout.write(
                self.style.SUCCESS(
                    'Фикстуры для таблицы Teacher созданы!',
                ),
        )
