from django.db import IntegrityError
from django.db.models.signals import post_save
from django.dispatch import receiver

from schooling.models import Student, Teacher
from potential_user.models import ApplicationForm


@receiver(post_save, sender=ApplicationForm)
def create_user_from_application(sender, instance, created, **kwargs):
    """Функция создания пользователя согласно роли в заявке."""
    if instance.approved and created:
        if instance.role == 'teacher':
            user_model = Teacher
        elif instance.role == 'student':
            user_model = Student
        try:
            user_model.objects.create(
                telegram_id=instance.telegram_id,
                name=instance.name,
                surname=instance.surname,
                city=instance.city,
                phone_number=instance.phone_number,
            )
        except IntegrityError as err:
            raise ValueError(
                f'Пользователь с telegram_id {instance.telegram_id} '
                'уже существует.',
            ) from err
