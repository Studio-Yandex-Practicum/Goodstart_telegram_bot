from django.db import models


class Subject(models.Model):
    """Модель для хранения школьных предметов."""

    name = models.CharField(
        max_length=128, unique=True, verbose_name="Название предмета"
    )
    subject_key = models.CharField(
        max_length=128, unique=True, blank=True, null=True
    )

    class Meta:
        verbose_name = "Название предмета"
        verbose_name_plural = "Названия предметов"

    def __str__(self):
        return self.name
