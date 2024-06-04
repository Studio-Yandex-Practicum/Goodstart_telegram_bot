from django.core.management.base import BaseCommand

from schooling.factories import create_lessons


class Command(BaseCommand):
    """Command to Lesson instances creation for the project tests."""

    def _generate(self):
        create_lessons()

    def handle(self, *args, **options):
        """Call the method `_generate` for the test Lesson creation."""
        self._generate()
