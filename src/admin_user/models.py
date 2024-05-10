from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from .managers import UserManager

DEFAULT_NAME_LENGTH = 150
EMAIL_LENGTH = 254


class Administrator(AbstractUser):
    """Custom Administrator model."""

    username = None
    first_name = models.CharField('Имя', max_length=DEFAULT_NAME_LENGTH)
    last_name = models.CharField('Фамилия', max_length=DEFAULT_NAME_LENGTH)
    phone = PhoneNumberField('Номер телефона', help_text='Формат +7XXXXXXXXXX')
    email = models.EmailField(
        'E-mail адрес',
        max_length=EMAIL_LENGTH,
        unique=True,
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('first_name', 'last_name', 'phone')

    class Meta:
        """
        Set verbose name and verbose name plural.

        Defaults to ordering by id.
        """

        ordering = ('id',)
        verbose_name = 'Администратор'
        verbose_name_plural = 'Администраторы'

    def __str__(self) -> str:
        """Return a string representation of User object."""
        return f'{self.first_name} {self.last_name}'
