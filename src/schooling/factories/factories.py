import random

import factory
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyInteger

from schooling.models import Student, StudyClass, Subject
from .constants import (
    START_PHONE_VALUE,
    END_PHONE_VALUE,
    STUDENTS_CREATION_COUNT,
    START_TELEGRAM_ID_VALUE,
    END_TELEGRAM_ID_VALUE,
    START_RANDOM_VALUE,
    STOP_RANDOM_VALUE,
)


class StudentFactory(DjangoModelFactory):
    """Factory of `Student` for the project testing."""

    class Meta:
        model = Student

    telegram_id = factory.Sequence(
        lambda id_tel: FuzzyInteger(
            START_TELEGRAM_ID_VALUE, END_TELEGRAM_ID_VALUE
        ).fuzz()
    )
    name = factory.Faker('first_name')
    surname = factory.Faker('last_name')
    city = factory.Faker('city')
    phone_number = factory.Sequence(
        lambda some: f'+7495{FuzzyInteger(
            START_PHONE_VALUE, END_PHONE_VALUE,
        ).fuzz()}',
    )
    study_class_id = factory.Iterator(StudyClass.objects.all())
    paid_lessons = FuzzyInteger(START_RANDOM_VALUE, STOP_RANDOM_VALUE)
    parents_contacts = factory.List([
        factory.Faker('name'),
        factory.Sequence(
        lambda some: f'+7495{FuzzyInteger(
            START_PHONE_VALUE, END_PHONE_VALUE,
        ).fuzz()}',
    )
    ])

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override default `_create` method to set subjects."""
        subject = Subject.objects.order_by('?')[
            :random.randint(START_RANDOM_VALUE, STOP_RANDOM_VALUE)
        ]
        student = super()._create(model_class, *args, **kwargs)
        student.subjects.set(subject)
        student.save()
        return student


def create_students():
    """Create `Student` instances for the project tests."""
    StudentFactory.create_batch(size=STUDENTS_CREATION_COUNT)
