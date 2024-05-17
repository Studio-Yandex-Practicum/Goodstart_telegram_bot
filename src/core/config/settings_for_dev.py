"""Settings for development."""

from core.config.settings_base import *  # noqa

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': env.str(
            'POSTGRES_ENGINE',
            default='django.db.backends.postgresql',
        ),
        'NAME': env.str('POSTGRES_NAME', default='postgres'),
        'USER': env.str('POSTGRES_USER', default='postgres'),
        'PASSWORD': env.str('POSTGRES_PASSWORD', default='postgres'),
        'HOST': env('POSTGRES_HOST', default='localhost'),
        'PORT': env('POSTGRES_PORT', default='5432'),
    },
}
