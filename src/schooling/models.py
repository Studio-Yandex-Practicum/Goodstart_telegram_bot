from datetime import  timedelta
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from bot.states import UserStates


MAX_LEN_NAME_SURNAME = 150
MAX_LEN_CITY = 50
MAX_LEN_STATE = 50


class GeneralUserModel(models.Model):
    """Базовая, абстрактная модель пользователя."""

    telegram_id = models.BigIntegerField('Telegram ID', unique=True)
    name = models.CharField('Имя', max_length=MAX_LEN_NAME_SURNAME)
    surname = models.CharField('Фамилия', max_length=MAX_LEN_NAME_SURNAME)
    city = models.CharField('Город', max_length=MAX_LEN_CITY)
    phone_number = PhoneNumberField('Номер телефона')
    last_login_date = models.DateField('Последнее посещение', auto_now=True)
    registration_date = models.DateField('Дата регистрации', auto_now_add=True)
    state = models.CharField(
        'Состояние пользователя',
        max_length=MAX_LEN_STATE,
        choices=UserStates.choices,
        default=UserStates.START,
    )

    class Meta:
        """Meta class of GeneralUserModel."""

        abstract = True

    def __str__(self):
        """Return a general user string representation."""
        return f'{self.name} {self.surname} {self.telegram_id}'


class Teacher(GeneralUserModel):
    """Модель преподавателя."""

    competence = models.ManyToManyField(
        'Subject',
        verbose_name='Предмет',
    )
    study_classes = models.ManyToManyField(
        'StudyClass',
        verbose_name='Учебный класс',
    )

    class Meta:
        """Meta class of TeacherModel."""

        verbose_name = 'преподаватель'
        verbose_name_plural = 'Преподаватели'

    def __str__(self):
        """Return a teacher string representation."""
        return f'{self.name} {self.surname}'


class Student(GeneralUserModel):
    """Модель студента."""

    study_class_id = models.ForeignKey(
        'StudyClass',
        on_delete=models.PROTECT,
        verbose_name='ID учебного класса',
        related_name='students',
        null=True,
        )
    paid_lessons = models.PositiveIntegerField(
        'Оплаченые занятия',
        default=0,
    )
    parents_contacts = models.CharField(
        max_length=256,  # Переписать значение!
        verbose_name='Контакты представителей',
        )
    subjects = models.ManyToManyField(
        'Subject',
        verbose_name='Предмет',
    )

    class Meta:
        """Meta class of StudentModel."""

        verbose_name = 'студент'
        verbose_name_plural = 'Студенты'

    def __str__(self):
        """Return a student string representation."""
        return f'{self.name} {self.surname}'


class Subject(models.Model):
    """Модель для хранения школьных предметов."""

    name = models.CharField(
        max_length=128,
        unique=True,
        verbose_name='Название предмета',
    )
    subject_key = models.CharField(
        max_length=128,
        unique=True,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'название предмета'
        verbose_name_plural = 'Названия предметов'

    def __str__(self):
        """Return a subject string representation."""
        return self.name


class StudyClass(models.Model):
    """Модель для хранения школьных классов."""

    study_class_name = models.CharField(
        max_length=64,
        unique=True,
        verbose_name='Название учебного класса',
    )
    study_class_number = models.PositiveIntegerField(
        verbose_name='Номер учебного класса',
    )

    class Meta:
        verbose_name = 'учебный класс'
        verbose_name_plural = 'Учебные классы'

    def __str__(self):
        """Return a studyclass string representation."""
        return self.study_class_name


class Lesson(models.Model):
    """Модель для хранения информации о занятиях."""

    name = models.CharField('Название занятия', max_length=256)
    subject = models.ForeignKey(
        'Subject',
        on_delete=models.CASCADE,
        verbose_name='Предмет',
        related_name='lessons',
    )
    teacher_id = models.ForeignKey(
        'Teacher',
        on_delete=models.CASCADE,
        verbose_name='Преподаватель',
        related_name='lessons',
    )
    student_id = models.ForeignKey(
        'Student',
        on_delete=models.CASCADE,
        verbose_name='Студент',
        related_name='lessons',
    )
    datetime_start = models.DateTimeField('Время начала занятия')
    duration = models.PositiveIntegerField('Продолжительность занятия')
    is_passed = models.BooleanField('Занятие прошло', default=False)
    test_lesson = models.BooleanField('Тестовое занятие', default=False)

    class Meta:
        """Meta class of LessonModel."""

        verbose_name = 'занятие'
        verbose_name_plural = 'Занятия'
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'name',
                    'subject',
                    'teacher_id',
                    'student_id',
                    'datetime_start',
                    'duration',
                ],
                name='unique_lesson',
            ),
        ]

    def __str__(self):
        """Return a lesson string representation."""
        return f'{self.name} {self.subject.name}'

    @property
    def datetime_end(self):
        """Returns the datetime end lesson."""
        return self.datetime_start + timedelta(minutes=self.duration)
