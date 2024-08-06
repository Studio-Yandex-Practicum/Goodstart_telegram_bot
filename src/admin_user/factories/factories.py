import factory
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyInteger

from admin_user.models import Administrator

from .constants import (
    ADMIN_CREATION_INSTANCES_COUNT,
    END_PHONE_NUMBER_VALUE,
    START_PHONE_NUMBER_VALUE,
)


class AdminFactory(DjangoModelFactory):
    """Factory of `Administrator` for the project testing."""

    class Meta:
        model = Administrator

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    phone = factory.Sequence(
        lambda some: f'+7495{FuzzyInteger(
            START_PHONE_NUMBER_VALUE,
            END_PHONE_NUMBER_VALUE,
        ).fuzz()}',
    )
    email = factory.LazyAttribute(
        lambda a: f'{a.first_name}.{a.last_name}@example.com'.lower(),
    )

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override default `_create` method to set password."""
        password = kwargs.pop('password', None)
        administrator = super()._create(model_class, *args, **kwargs)
        administrator.set_password(password)
        administrator.is_staff = True
        administrator.save()
        return administrator


def create_admins():
    """Create `Administrator` instances for the project tests."""
    AdminFactory.create_batch(size=ADMIN_CREATION_INSTANCES_COUNT)
