from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


MAX_LEN_NAME_SURNAME = 150
MAX_LEN_CITY = 50


class GeneralUserModel(models.Model):
    """Базовая, абстрактная модель пользователя."""

    telegram_id = models.BigIntegerField('Telegram ID', unique=True)
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
        'Subject',
        verbose_name='Предмет',
    )
    study_classes = models.ManyToManyField(
        'StudyClass',
        verbose_name='Учебный класс',
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
        'StudyClass',
        # TODO После реализации модели StudyClass проработать правило удаления
        on_delete=models.DO_NOTHING,
        verbose_name='ID учебного класса',
        related_name='students',
        null=True,
        # Установить либо значение по умолчанию, либо blank=True
        )
    paid_lessons = models.PositiveIntegerField(
        'Оплаченые занятия',
        default=0
    )
    parents_contacts = models.CharField(
        max_length=256,  # Переписать значение!
        verbose_name='Контакты представителей',
        # Установить либо значение по умолчанию, либо blank=True
        )
    subjects = models.ManyToManyField(
        'Subject',
        verbose_name='Предмет',
    )

    class Meta:
        """Meta class of StudentModel."""

        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'

    def __str__(self):
        """Return a student string representation."""
        return f'{self.name} {self.surname} {self.subjects}'


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
        verbose_name = 'Название предмета'
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
        verbose_name='ID преподавателя',
        related_name='lessons',
    )
    student_id = models.ForeignKey(
        'Student',
        on_delete=models.CASCADE,
        verbose_name='ID студента',
        related_name='lessons',
    )
    datetime_start = models.DateTimeField('Время начала занятия')
    datetime_end = models.DateTimeField('Время окончания занятия')
    is_passed = models.BooleanField('Занятие прошло', default=False)
    test_lesson = models.BooleanField('Тестовое занятие', default=False)

    class Meta:
        """Meta class of LessonModel."""

        verbose_name = 'Занятие'
        verbose_name_plural = 'Занятия'
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'name',
                    'subject',
                    'teacher_id',
                    'student_id',
                    'datetime_start',
                    'datetime_end',
                ],
                name='unique_lesson',
            ),
        ]

    def __str__(self):
        """Return a lesson string representation."""
        return f'{self.name} {self.subject.name}'
