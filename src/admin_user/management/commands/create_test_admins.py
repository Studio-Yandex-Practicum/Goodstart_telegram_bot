from admin_user.factories import create_admins
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Command to Administrator instances creation for the project tests."""

    def _generate(self):
        create_admins()

    def handle(self, *args, **options):
        self._generate()
