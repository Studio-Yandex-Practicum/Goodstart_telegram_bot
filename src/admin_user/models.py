from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from admin_user.managers import UserManager
from schooling.validators.phone_validators import validate_phone_number

DEFAULT_NAME_LENGTH = 150
EMAIL_LENGTH = 254


class Administrator(AbstractBaseUser, PermissionsMixin):
    """Custom Administrator model."""

    username = None
    first_name = models.CharField(
        verbose_name=_('Имя.'),
        max_length=DEFAULT_NAME_LENGTH,
    )
    last_name = models.CharField(
        verbose_name=_('Фамилия.'),
        max_length=DEFAULT_NAME_LENGTH,
    )
    phone = PhoneNumberField(
        verbose_name=_('Номер телефона.'),
        validators=[validate_phone_number],
        help_text='Формат +7XXXXXXXXXX',
    )
    email = models.EmailField(
        verbose_name=_('Email адрес.'),
        max_length=EMAIL_LENGTH,
        unique=True,
    )
    date_joined = models.DateTimeField(
        default=timezone.now,
        verbose_name=_('Дата регистрации.'),
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name=_('Статус администратора.'),
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('Показывает статус он-лайн.'),
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = (
        'first_name',
        'last_name',
        'phone',
    )

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
