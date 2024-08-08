import random
from datetime import datetime, timedelta

import factory
from django.core.exceptions import ObjectDoesNotExist
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

    telegram_id = FuzzyInteger(START_TELEGRAM_ID_VALUE,
                               END_TELEGRAM_ID_VALUE)
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
            ).fuzz()}',),])

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
            # Проверяем, был ли datetime_start уже установлен
            if not self.datetime_start:
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

    @classmethod
    def create_personal_lessons(cls, telegram_id):
        """Создает случайные уроки для ученика по его telegram_id."""
        try:
            student = Student.objects.get(telegram_id=telegram_id)
        except ObjectDoesNotExist:
            return

        start_date = timezone.now().date() - timedelta(
            days=timezone.now().date().weekday() + 7)
        end_date = timezone.now().date() + timedelta(
            days=(13 - timezone.now().date().weekday()))

        lessons_to_create = []
        for n in range(int((end_date - start_date).days)):
            date = start_date + timedelta(n)
            for _ in range(random.randint(1, 3)):
                subject = student.subjects.order_by('?').first()
                if not subject:
                    continue
                teacher = (
                    Teacher.objects.filter(competence=subject)
                    .order_by('?')
                    .first()
                )
                if not teacher:
                    continue
                lesson_time_aware = timezone.make_aware(
                    datetime.combine(
                        date,
                        timezone.now()
                        .time()
                        .replace(
                            hour=random.randint(8, 18),
                            minute=random.randint(0, 55) // 5 * 5,
                        ),))
                is_passed = lesson_time_aware < timezone.now()
                lesson = cls(
                    id=None,
                    student_id=student,
                    datetime_start=lesson_time_aware,
                    is_passed=is_passed,
                    subject=subject,
                    teacher_id=teacher,
                )
                lessons_to_create.append(lesson)

        Lesson.objects.bulk_create(lessons_to_create, ignore_conflicts=True)


def create_students():
    """Create `Student` instances for the project tests."""
    StudentFactory.create_batch(size=CREATION_COUNT)


def create_teachers():
    """Create `Teacher` instances for the project tests."""
    TeacherFactory.create_batch(size=CREATION_COUNT)


def create_lessons():
    """Create `Lesson` instances for the project tests."""
    LessonFactory.create_batch(size=CREATION_COUNT)
