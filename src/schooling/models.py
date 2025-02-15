from datetime import timedelta

from django.core.exceptions import ValidationError
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from bot.states import UserStates
from schooling.validators.phone_validators import validate_phone_number


MAX_LEN_NAME_SURNAME = 150
MAX_LEN_CITY = 50
MAX_LEN_STATE = 50
MAX_COUNT_STUDENTS = 30
MAX_COUNT_CLASSES = 5
MAX_COUNT_SUBJECTS = 3
DEFAULT_LESSON_DURATION = 60


class GeneralUserModel(models.Model):
    """Базовая, абстрактная модель пользователя."""

    telegram_id = models.BigIntegerField('Telegram ID', unique=True)
    name = models.CharField('Имя', max_length=MAX_LEN_NAME_SURNAME)
    surname = models.CharField('Фамилия', max_length=MAX_LEN_NAME_SURNAME)
    city = models.CharField('Город', max_length=MAX_LEN_CITY)
    phone_number = PhoneNumberField(
        'Номер телефона',
        validators=[validate_phone_number],
        help_text='Формат +7XXXXXXXXXX',
    )
    last_login_date = models.DateField('Последнее посещение', auto_now=True)
    registration_date = models.DateField('Дата регистрации', auto_now_add=True)
    state = models.CharField(
        'Состояние пользователя',
        max_length=MAX_LEN_STATE,
        choices=UserStates.choices,
        default=UserStates.START,
    )

    class Meta:
        abstract = True

    def __str__(self):
        """Возвращает общее строковое представление пользователя."""
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
        verbose_name = 'Преподаватель'
        verbose_name_plural = 'Преподаватели'

    def __str__(self):
        """Возвращает полное имя преподавателя."""
        return f'{self.name} {self.surname}'

    def clean(self):
        """
        Проверка на максимальное количество классов и предметов.

        Осуществляется на одного преподавателя.
        """
        current_classes_count = self.study_classes.count()
        current_subjects_count = self.competence.count()

        if current_classes_count > MAX_COUNT_CLASSES:
            raise ValidationError(
                f'Преподаватель {self.name} {self.surname} уже '
                f'ведет максимальное количество классов.')

        if current_subjects_count > MAX_COUNT_SUBJECTS:
            raise ValidationError(
                f'Преподаватель {self.name} {self.surname} уже '
                f'ведет максимальное количество предметов.')


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
        max_length=256,
        verbose_name='Контакты представителей',
    )
    subjects = models.ManyToManyField(
        'Subject',
        verbose_name='Предмет',
    )

    class Meta:

        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'

    def __str__(self):
        """Возвращает строковое представление студента."""
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
        """Возвращает строковое представление предмета."""
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
        """Возвращает название учебного класса."""
        return self.study_class_name

    def clean(self):
        """Проверка на максимальное количество студентов в одном классе."""
        current_students_count = self.students.count()

        if current_students_count > MAX_COUNT_STUDENTS:
            raise ValidationError(
                f'Максимальное количество студентов в классе '
                f'"{self.study_class_name}" уже достигнуто.',
            )


class LessonGroup(models.Model):
    """Модель группы занятий, связывающая студента с его занятиями."""

    student = models.ForeignKey(
        'Student',
        on_delete=models.CASCADE,
        verbose_name='Студент',
        related_name='lesson_groups',
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата создания',
    )

    class Meta:
        verbose_name = 'группа занятий'
        verbose_name_plural = 'Группы занятий'

    def __str__(self):
        """Возвращает строковое представление группы занятий."""
        return f'Группа занятий {self.student.name} {self.student.surname}'


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
    group = models.ForeignKey(
        'LessonGroup',
        on_delete=models.CASCADE,
        verbose_name='Группа занятий',
        related_name='lessons',
        null=True,
    )
    datetime_start = models.DateTimeField('Время начала занятия')
    duration = models.PositiveIntegerField(
        'Продолжительность занятия',
        help_text='Продолжительность занятия в минутах.',
        default=DEFAULT_LESSON_DURATION,
    )
    lesson_count = models.PositiveIntegerField(
        'Количество создаваемых занятий',
        default=1,
        help_text='Сколько занятий создать',
    )
    is_passed = models.BooleanField('Занятие прошло', default=False)
    video_meeting_url = models.URLField(
        'Ссылка на проведение урока',
        help_text='Там, где будет проходить встреча',
        null=True,
    )
    homework_url = models.URLField(
        'Ссылка на домашнее задание',
        help_text='Там, где размещено домашнее задание',
        null=True,
    )
    is_passed_teacher = models.BooleanField(
        'Занятие подтверждено учителем', default=False,
    )
    is_passed_student = models.BooleanField(
        'Занятие подтверждено учеником', default=False,
    )
    test_lesson = models.BooleanField('Пробное занятие', default=False)
    regular_lesson = models.BooleanField(
        'Регулярное занятие', default=False,
    )

    class Meta:
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
        unique_together = ('name', 'datetime_start')
        verbose_name = 'занятие'
        verbose_name_plural = 'Занятия'

    def __str__(self):
        """Возвращает строковое представление занятия."""
        return f'{self.name} {self.subject.name}'

    def clean(self):
        """Проверка на совпадение занятия с уже существующими."""
        if Lesson.objects.filter(
            name=self.name,
            datetime_start__date=self.datetime_start.date(),
        ).exclude(pk=self.pk).exists():
            raise ValidationError(
                'Урок с таким названием уже существует в этот день.',
            )

    def save(self, *args, **kwargs):
        """Проверка на группу и на создание повторяющихся занятий."""
        if not self.group:
            self.group = self.get_or_create_group()
        super().save(*args, **kwargs)
        if self.lesson_count > 1:
            self.create_lessons()

    @property
    def datetime_end(self):
        """Возвращает дату и время окончания урока."""
        return self.datetime_start + timedelta(minutes=self.duration)

    def get_or_create_group(self):
        """Возвращает существующую группу студента или создаёт новую."""
        group = LessonGroup.objects.filter(
            student=self.student_id,
            lessons__subject=self.subject,
        ).first()
        if not group:
            group = LessonGroup.objects.create(student=self.student_id)
        return group

    def create_lessons(self):
        """Создаёт несколько занятий на основе lesson_count."""
        if self.lesson_count < 1:
            raise ValidationError(
                'Количество создаваемых занятий должно быть больше 0.',
            )
        lesson_group = self.get_or_create_group()
        lessons = [
            Lesson(
                name=self.name,
                subject=self.subject,
                teacher_id=self.teacher_id,
                student_id=self.student_id,
                group=lesson_group,
                datetime_start=self.datetime_start + timedelta(days=i + 1),
                duration=self.duration,
                is_passed=False,
                video_meeting_url=self.video_meeting_url,
                homework_url=self.homework_url,
                is_passed_teacher=False,
                is_passed_student=False,
                test_lesson=self.test_lesson,
                regular_lesson=self.regular_lesson,
            )
            for i in range(self.lesson_count - 1)
        ]
        Lesson.objects.bulk_create(lessons)
