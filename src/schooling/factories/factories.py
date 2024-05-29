import random

import factory
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyInteger

from schooling.models import Student, StudyClass, Subject, Teacher
from .constants import (
    START_PHONE_VALUE,
    END_PHONE_VALUE,
    CREATION_COUNT,
    START_TELEGRAM_ID_VALUE,
    END_TELEGRAM_ID_VALUE,
    START_RANDOM_VALUE,
    STOP_RANDOM_VALUE,
    LOCALE,
)


class PersonFactory(DjangoModelFactory):
    """Absctract Class for factory of Person for the project testing."""

    class Meta:
        abstract = True

    telegram_id = FuzzyInteger(START_TELEGRAM_ID_VALUE, END_TELEGRAM_ID_VALUE)
    name = factory.Faker('first_name', locale=LOCALE)
    surname = factory.Faker('last_name', locale=LOCALE)
    city = factory.Faker('city', locale=LOCALE)
    phone_number = factory.Sequence(
        lambda some: f'+7495{FuzzyInteger(
            START_PHONE_VALUE, END_PHONE_VALUE,
        ).fuzz()}',
    )


class StudentFactory(PersonFactory):
    """Factory of `Student` for the project testing."""

    class Meta:
        model = Student

    study_class_id = factory.Iterator(StudyClass.objects.all())
    paid_lessons = FuzzyInteger(START_RANDOM_VALUE, STOP_RANDOM_VALUE)
    parents_contacts = factory.List([
        factory.Faker('name', locale=LOCALE),
        factory.Sequence(
            lambda some: f'+7495{FuzzyInteger(
                START_PHONE_VALUE, END_PHONE_VALUE,
            ).fuzz()}',
        ),
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


class TeacherFactory(PersonFactory):
    """Factory of `Teacher` for the project testing."""

    class Meta:
        model = Teacher

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override `_create` method to set competence and study classes."""
        competence = Subject.objects.order_by('?')[
            :random.randint(START_RANDOM_VALUE, STOP_RANDOM_VALUE)
        ]
        study_classes = StudyClass.objects.order_by('?')[
            :random.randint(START_RANDOM_VALUE, STOP_RANDOM_VALUE)
        ]
        teacher = super()._create(model_class, *args, **kwargs)
        teacher.competence.set(competence)
        teacher.study_classes.set(study_classes)
        teacher.save()
        return teacher


def create_students():
    """Create `Student` instances for the project tests."""
    StudentFactory.create_batch(size=CREATION_COUNT)


def create_teachers():
    """Create `Student` instances for the project tests."""
    TeacherFactory.create_batch(size=CREATION_COUNT)
