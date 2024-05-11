from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class ApplicationForm(models.Model):
    """Модель регистрации пользователей. Роль устанавливает администратор."""

    ROLE_CHOICES = (
        ('teacher', 'Преподаватель'),
        ('student', 'Учащийся'),
    )

    telegram_id = models.IntegerField('Telegram ID', unique=True, help_text='Введите свой ID')
    role = models.CharField('Роль', choices=ROLE_CHOICES, max_length=20)
    name = models.CharField('Имя', max_length=20, help_text="Обязательное поле")
    surname = models.CharField('Фамилия', max_length=20, help_text="Обязательное поле")
    city = models.CharField('Город', max_length=20)
    phone_number = PhoneNumberField('Номер телефона')
    approved = models.BooleanField(default=False)

    class Meta:
        """Meta class of ApplicationForm."""

        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'

    def __str__(self):
        """Return a string representation."""
        return f'{self.name} {self.surname} {self.role}'
