from django.contrib.auth.models import AbstractUser
from django.db import models
from phone_field import PhoneField

DEFAULT_NAME_LENGTH = 150
EMAIL_LENGTH = 254


class Administator(AbstractUser):
    """Custom administator model."""

    first_name = models.CharField("Имя", max_length=DEFAULT_NAME_LENGTH)
    last_name = models.CharField("Фамилия", max_length=DEFAULT_NAME_LENGTH)
    phone = PhoneField("Номер телефона", help_text="Формат +7XXXXXXXXXX")
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("username", "first_name", "last_name", "phone")

    email = models.EmailField(
        "E-mail адрес",
        max_length=EMAIL_LENGTH,
        unique=True,
    )

    class Meta:
        """Set verbose name and verbose name plural.

        Defaults to ordering by id.
        """

        ordering = ("id",)
        verbose_name = "Администратор"
        verbose_name_plural = "Администраторы"

    def __str__(self) -> str:
        """Return a string representation of User object."""
        return self.username
