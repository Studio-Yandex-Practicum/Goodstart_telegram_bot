from django.db import models


class StudyClass(models.Model):
    """Модель для хранения школьных классов."""

    study_class_name = models.CharField(
        max_length=64,
        unique=True,
        verbose_name='Название учебного класса'
    )
    study_class_number = models.PositiveIntegerField(
        verbose_name='Номер учебного класса'
    )

    def __str__(self):
        """Return a studyclass string representation."""
        return self.study_class_name
