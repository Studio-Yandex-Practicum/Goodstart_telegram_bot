from django.core.management.base import BaseCommand

from schooling.factories import create_students


class Command(BaseCommand):
    """Command to Student instances creation for the project tests."""

    def _generate(self):
        create_students()

    def handle(self, *args, **options):
        """Call the method `_generate` for the test Student creation."""
        self._generate()
        return self.stdout.write(
                self.style.SUCCESS(
                    'Фикстуры для таблицы Student созданы!',
                ),
        )
