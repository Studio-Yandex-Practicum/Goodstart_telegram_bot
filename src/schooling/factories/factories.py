import os
import random
from datetime import datetime, timedelta

import factory
from django.db.models.signals import post_save
from django.utils import timezone
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyInteger

from schooling.models import Lesson, Student, StudyClass, Subject, Teacher

from .constants import (
    CREATION_COUNT,
    END_PHONE_VALUE,
    END_TELEGRAM_ID_VALUE,
    LOCALE,
    START_PHONE_VALUE,
    START_RANDOM_VALUE,
    START_TELEGRAM_ID_VALUE,
    STOP_RANDOM_VALUE,
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


@factory.django.mute_signals(post_save)
class StudentFactory(PersonFactory):
    """Factory of `Student` for the project testing."""

    class Meta:
        model = Student

    study_class_id = factory.Iterator(StudyClass.objects.all())
    paid_lessons = FuzzyInteger(START_RANDOM_VALUE, STOP_RANDOM_VALUE)
    parents_contacts = factory.List(
        [
            factory.Faker('name', locale=LOCALE),
            factory.Sequence(
                lambda some: f'+7495{FuzzyInteger(
                START_PHONE_VALUE, END_PHONE_VALUE,
            ).fuzz()}',
            ),
        ]
    )

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override default `_create` method to set subjects."""
        subject = Subject.objects.order_by('?')[
            : random.randint(START_RANDOM_VALUE, STOP_RANDOM_VALUE)
        ]
        student = super()._create(model_class, *args, **kwargs)
        student.subjects.set(subject)
        student.save()
        return student


@factory.django.mute_signals(post_save)
class TeacherFactory(PersonFactory):
    """Factory of `Teacher` for the project testing."""

    class Meta:
        model = Teacher

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override `_create` method to set competence and study classes."""
        competence = Subject.objects.order_by('?')[
            : random.randint(START_RANDOM_VALUE, STOP_RANDOM_VALUE)
        ]
        study_classes = StudyClass.objects.order_by('?')[
            : random.randint(START_RANDOM_VALUE, STOP_RANDOM_VALUE)
        ]
        teacher = super()._create(model_class, *args, **kwargs)
        teacher.competence.set(competence)
        teacher.study_classes.set(study_classes)
        teacher.save()
        return teacher


class LessonFactory(DjangoModelFactory):
    """Factory of `Lesson` for the project testing."""

    class Meta:
        model = Lesson

    name = factory.Faker('sentence', nb_words=1, locale='ru_RU')
    teacher_id = factory.SubFactory(TeacherFactory)
    student_id = factory.SubFactory(StudentFactory)
    is_passed = factory.LazyAttribute(lambda o: random.choice([True, False]))
    test_lesson = factory.LazyAttribute(lambda o: random.choice([True, False]))
    datetime_start = timezone.now()
    duration = 60

    @factory.post_generation
    def datetime_start_and_end(self, create, extracted, **kwargs):
        """Добавляет дату и время урока и его продолжительность."""
        if create:
            if self.is_passed:
                self.datetime_start = timezone.now() - timedelta(days=365)
            else:
                self.datetime_start = timezone.now() + timedelta(days=365)

    @factory.lazy_attribute
    def subject(self):
        """Получить случайный учебный предмет."""
        subject = Subject.objects.order_by('name')[
            random.randint(START_RANDOM_VALUE, STOP_RANDOM_VALUE)
        ]
        return subject


def create_students():
    """Create `Student` instances for the project tests."""
    StudentFactory.create_batch(size=CREATION_COUNT)


def create_teachers():
    """Create `Teacher` instances for the project tests."""
    TeacherFactory.create_batch(size=CREATION_COUNT)


def create_lessons():
    """Create `Lesson` instances for the project tests."""
    LessonFactory.create_batch(size=CREATION_COUNT)


def create_personal_lessons():
    """Create `Lesson` instances for the project tests."""
    student = Student.objects.get(telegram_id=os.getenv('TELEGRAM_ID'))
    teachers = list(Teacher.objects.all())
    days_to_generate = [
        timezone.now().date() + timedelta(days=i) for i in range(-7, 14)
    ]
    competent_subjects = Subject.objects.filter(
        teacher__in=teachers
    ).distinct()

    for day in days_to_generate:
        number_of_lessons = random.randint(1, 5)
        for _ in range(number_of_lessons):
            lesson_start_time = timezone.make_aware(
                datetime.combine(
                    day,
                    timezone.now()
                    .time()
                    .replace(
                        hour=random.randint(8, 18),
                        minute=random.randint(0, 55) // 5 * 5,
                    ),
                )
            )
            if competent_subjects:
                subject = random.choice(list(competent_subjects))
                LessonFactory.create(
                    student_id=student,
                    datetime_start=lesson_start_time,
                    teacher_id=random.choice(teachers),
                    subject=subject,
                )
