from django.core.management.base import BaseCommand

from admin_user.factories import create_admins


class Command(BaseCommand):
    """Command to Administrator instances creation for the project tests."""

    def _generate(self):
        create_admins()

    def handle(self, *args, **options):
        """Call the method `_generate` for the test Admin creation."""
        self._generate()
        return self.stdout.write(
                self.style.SUCCESS(
                    'Фикстуры для таблицы Administrator созданы!',
                ),
        )
