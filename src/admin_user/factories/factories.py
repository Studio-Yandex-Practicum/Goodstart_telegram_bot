import factory
from factory.fuzzy import FuzzyInteger
from factory.django import DjangoModelFactory

from admin_user.models import Administrator
from admin_user.constants import (
    ADMIN_CREATION_INSTANCES_COUNT,
    START_PHONE_NUMBER_VALUE,
    END_PHONE_NUMBER_VALUE,
)


class AdminFactory(DjangoModelFactory):
    """
    Factory of Admin for the project testing.
    """

    class Meta:
        model = Administrator

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    phone = factory.Sequence(
        lambda some: f'+7495{FuzzyInteger(
            START_PHONE_NUMBER_VALUE,
            END_PHONE_NUMBER_VALUE,
        ).fuzz()}'
    )
    email = factory.LazyAttribute(
        lambda a: f'{a.first_name}.{a.last_name}@example.com'.lower()
    )
    username = factory.Faker('user_name', locale='ru_RU')

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override default _create method to set password."""
        password = kwargs.pop('password', None)
        administrator = super()._create(model_class, *args, **kwargs)
        administrator.set_password(password)
        administrator.is_staff = True
        administrator.save()
        return administrator


def create_admins():
    """Create Administrator instances for the project tests"""
    AdminFactory.create_batch(size=ADMIN_CREATION_INSTANCES_COUNT)
