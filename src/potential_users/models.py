from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class ApplicationForm(models.Model):
    """Модель регистрации пользователей. Роль устанавливает администратор."""

    ROLE_CHOICES = (
        ("teacher", "Преподаватель"),
        ("student", "Учащийся"),
    )

    telegram_id = models.IntegerField("Telegram ID", unique=True)
    role = models.CharField(choices=ROLE_CHOICES)
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    phone_number = PhoneNumberField()
    approved = models.BooleanField(default=False)

    class Meta:
        """Meta class of ApplicationForm."""

        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"

    def __str__(self):
        """Return a string representation."""
        return f"{self.name} {self.surname} {self.role}"
