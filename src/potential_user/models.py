from django.core.exceptions import ValidationError
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from schooling.models import StudyClass
from schooling.validator import validate_phone_number


class ApplicationForm(models.Model):
    """Модель регистрации пользователей. Роль устанавливает администратор."""

    ROLE_CHOICES = (
        ('teacher', 'Преподаватель'),
        ('student', 'Учащийся'),
    )
    telegram_id = models.PositiveBigIntegerField(
        'Telegram ID',
        unique=True,
        help_text='Введите свой ID',
    )
    role = models.CharField(
        'Роль',
        choices=ROLE_CHOICES,
        max_length=20,
    )
    name = models.CharField(
        'Имя',
        max_length=20,
        help_text='Обязательное поле',
    )
    surname = models.CharField(
        'Фамилия',
        max_length=20,
        help_text='Обязательное поле',
    )
    city = models.CharField(
        'Город',
        max_length=20,
    )
    phone_number = PhoneNumberField(
        'Номер телефона',
        validators=[validate_phone_number],
        help_text='Формат +7XXXXXXXXXX',
    )
    study_class_id = models.ForeignKey(
        StudyClass,
        on_delete=models.DO_NOTHING,
        verbose_name='ID учебного класса',
        related_name='potential_user',
        blank=True,
        null=True,
        )
    parents_contacts = models.CharField(
        max_length=256,  # Переписать значение!
        verbose_name='Контакты представителей',
        blank=True,
        null=True,
        )

    approved = models.BooleanField('Принять заявку', default=False)

    class Meta:
        """Meta class of ApplicationForm."""

        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'

    def __str__(self):
        """Return a string representation."""
        return f'{self.name} {self.surname} {self.role}'

    def validate_constraints(self, exclude) -> None:
        """Валидатор для роли Студента."""
        if (self.role == 'student'
            and self.approved
            and (not self.parents_contacts
                 or not self.study_class_id)):
            raise ValidationError('Для роли Студент поля "ID учебного класса" '
                                  'и "Контакты представителей должны быть'
                                  ' заполнены перед одобрением заявки!"')
        return super().validate_constraints(exclude)
