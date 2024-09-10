from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    """Менеджер для модели пользователя."""

    def create_user(self, email, password=None, **extra_fields):
        """Создает обычного пользователя с заданным email и паролем."""
        if not email:
            raise ValueError('Пользователь должен иметь email')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """Создает суперпользователя с заданным email и паролем."""
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(
                'Суперпользователь должен иметь is_staff=True.',
            )
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(
                'Суперпользователь должен иметь is_superuser=True.',
            )

        return self.create_user(email, password, **extra_fields)
