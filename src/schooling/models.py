from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

MAX_LEN_NAME_SURNAME = 150
MAX_LEN_CITY = 50


class GeneralUserModel(models.Model):
    """Базовая, абстрактная модель пользователя."""

    telegram_id = models.IntegerField('Telegram ID', unique=True)
    name = models.CharField('Имя', max_length=MAX_LEN_NAME_SURNAME)
    surname = models.CharField('Фамилия', max_length=MAX_LEN_NAME_SURNAME)
    city = models.CharField('Город', max_length=MAX_LEN_CITY)
    phone_number = PhoneNumberField('Номер телефона')
    last_login_date = models.DateField('Последнее посещение', auto_now=True)
    registration_date = models.DateField('Дата регистрации', auto_now_add=True)

    class Meta:
        """Meta class of GeneralUserModel."""

        abstract = True

    def __str__(self):
        """Return a general user string representation."""
        return f'{self.name} {self.surname} {self.telegram_id}'


class Teacher(GeneralUserModel):
    """Модель преподавателя."""

    competence = models.ManyToManyField(
        'Subject', verbose_name='Предмет',
    )
    study_classes = models.ManyToManyField(
        'StudyClass', verbose_name='Учебный класс',
    )

    class Meta:
        """Meta class of TeacherModel."""

        verbose_name = 'Преподаватель'
        verbose_name_plural = 'Преподаватели'

    def __str__(self):
        """Return a teacher string representation."""
        return f'{self.name} {self.surname} {self.competence}'


class Student(GeneralUserModel):
    """Модель студента."""

    study_class_id = models.ForeignKey(
        'StudyClass', on_delete=models.SET_NULL,
        verbose_name='ID учебного класса', related_name='students',
    )
    paid_lessons = models.PositiveIntegerField('Оплаченые занятия')
    parents_contacts = models.CharField('Контакты представителей')
    subjects = models.ManyToManyField(
        'Subject', verbose_name='Предмет',
    )

    class Meta:
        """Meta class of StudentModel."""

        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'

    def __str__(self):
        """Return a student string representation."""
        return f'{self.name} {self.surname} {self.subjects}'
