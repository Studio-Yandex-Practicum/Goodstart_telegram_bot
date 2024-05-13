"""Settings for development."""

from core.config.settings_base import *  # noqa

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': env(
            'POSTGRES_ENGINE',
            default='django.db.backends.postgresql',
        ),
        'NAME': env('POSTGRES_NAME', default='postgres'),
        'USER': env('POSTGRES_USER', default='postgres'),
        'PASSWORD': 'postgres',
        'HOST': env('POSTGRES_HOST', default='localhost'),
        'PORT': env('POSTGRES_PORT', default='5432'),
    },
}
