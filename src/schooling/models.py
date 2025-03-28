from datetime import timedelta

from django.core.exceptions import ValidationError
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models.signals import post_delete
from django.dispatch import receiver

from bot.states import UserStates
from schooling.validators.phone_validators import validate_phone_number
from schooling.validators.file_size_validator import validate_file_size


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
        region='RU',
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
        ordering = ['name', 'surname']

    def __str__(self):
        """Возвращает полное имя преподавателя."""
        return f'{self.name} {self.surname}'

    def save(self, *args, **kwargs):
        """
        Сохраняет объект.

        Выполняет валидацию количества предметов и классов.
        """
        self.full_clean()
        super().save(*args, **kwargs)


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

        verbose_name = 'Ученик'
        verbose_name_plural = 'Ученики'
        ordering = ['name', 'surname']

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
        verbose_name='Ученик',
        related_name='lesson_groups',
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата создания',
    )

    class Meta:
        verbose_name = 'расписание'
        verbose_name_plural = 'Расписание'

    def __str__(self):
        """Возвращает строковое представление группы занятий."""
        return f'Расписание для {self.student.name} {self.student.surname}'


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
        on_delete=models.SET_NULL,
        verbose_name='Преподаватель',
        related_name='lessons',
        null=True,
    )
    student_id = models.ForeignKey(
        'Student',
        on_delete=models.CASCADE,
        verbose_name='Ученик',
        related_name='lessons',
    )
    group = models.ForeignKey(
        'LessonGroup',
        on_delete=models.CASCADE,
        verbose_name='Расписание',
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
        help_text='Указанное количество занятий будет '
                  'создано с интервалом в 1 неделю.',
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
    )  # Висит мертвым грузом пока не найдется применение.
    homework_text = models.TextField(
        'Текст домашнего задания',
        help_text='Описание домашнего задания',
        blank=True,
        null=True,
    )
    is_passed_teacher = models.BooleanField(
        'Занятие подтверждено учителем', default=False,
    )
    test_lesson = models.BooleanField('Пробное занятие', default=False)
    regular_lesson = models.BooleanField(
        'Регулярное занятие', default=False,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'subject',
                    'teacher_id',
                    'student_id',
                    'datetime_start',
                    'duration',
                ],
                name='unique_lesson',
            ),
        ]
        verbose_name = 'занятие'
        verbose_name_plural = 'Занятия'

    def __str__(self):
        """Возвращает строковое представление занятия."""
        return f'{self.name} {self.subject.name}'

    def save(self, *args, **kwargs):
        """Проверка на группу и на создание повторяющихся занятий."""
        if not self.group and self.student_id:
            self.group = self.get_or_create_group()
        super().save(*args, **kwargs)
        if self.lesson_count > 1:
            self.create_lessons()

    def clean(self):
        """Проверка на совпадение занятия с уже существующими."""
        if not self.datetime_start:
            raise ValidationError(
                'Дата начала занятия не может быть пустой.',
            )

    @property
    def datetime_end(self):
        """Возвращает дату и время окончания урока."""
        return self.datetime_start + timedelta(minutes=self.duration)

    def get_or_create_group(self):
        """Возвращает существующую группу студента или создаёт новую."""
        group, _ = LessonGroup.objects.get_or_create(student=self.student_id)
        return group

    def create_lessons(self):
        """Создаёт несколько занятий на основе lesson_count."""
        if self.lesson_count < 1:
            raise ValidationError(
                'Количество создаваемых занятий должно быть больше 0.',
            )
        lesson_group = self.get_or_create_group()
        lessons = []

        for i in range(1, self.lesson_count):
            new_datetime = self.datetime_start + timedelta(weeks=i)

            # Проверяем, существует ли уже такое занятие
            if Lesson.objects.filter(
                subject=self.subject,
                teacher_id=self.teacher_id,
                student_id=self.student_id,
                datetime_start=new_datetime,
                duration=self.duration,
            ).exists():
                continue  # Пропускаем создание дубликата

            lessons.append(
                Lesson(
                    name=self.name,
                    subject=self.subject,
                    teacher_id=self.teacher_id,
                    student_id=self.student_id,
                    group=lesson_group,
                    datetime_start=new_datetime,
                    duration=self.duration,
                    is_passed=False,
                    video_meeting_url=self.video_meeting_url,
                    is_passed_teacher=False,
                    test_lesson=self.test_lesson,
                    regular_lesson=self.regular_lesson,
                ),
            )

        if lessons:
            Lesson.objects.bulk_create(lessons)


class HomeworkImage(models.Model):
    """Изображения для домашнего задания."""

    lesson = models.ForeignKey(
        'Lesson',
        on_delete=models.CASCADE,
        related_name='homework_images',
        verbose_name='Урок',
    )
    image = models.ImageField(
        'Изображение',
        upload_to='lesson_homework/images/',
        validators=[validate_file_size],
    )

    class Meta:
        verbose_name = 'изображение'
        verbose_name_plural = 'изображения'

    def __str__(self):
        """Возвращает строковое представление изображения."""
        return f'Изображение для {self.lesson.name}'


class HomeworkFile(models.Model):
    """Файлы (PDF, DOCX и т. д.) для домашнего задания."""

    lesson = models.ForeignKey(
        'Lesson',
        on_delete=models.CASCADE,
        related_name='homework_files',
        verbose_name='Урок',
    )
    file = models.FileField(
        'Файл',
        upload_to='lesson_homework/files/',
        validators=[validate_file_size],
    )

    class Meta:
        verbose_name = 'файл'
        verbose_name_plural = 'файлы'

    def __str__(self):
        """Возвращает строковое представление файла."""
        return f'Файл для {self.lesson.name}'


@receiver(post_delete, sender=Lesson)
def delete_empty_lesson_group(sender, instance, **kwargs):
    """Удаляет группу занятий, если в ней больше нет занятий."""
    if instance.group_id:
        try:
            group = instance.group
            if not group.lessons.exists():
                group.delete()
        except LessonGroup.DoesNotExist:
            pass
