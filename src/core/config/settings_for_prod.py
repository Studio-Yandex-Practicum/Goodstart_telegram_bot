"""Settings for production."""

from core.config.settings_base import *  # noqa

DEBUG = env('DEBUG')

DATABASES = {
    'default': {
        'ENGINE': env.str(
            'DB_ENGINE',
            'django.db.backends.postgresql_psycopg2',
        ),
        'NAME': env.str('POSTGRES_DB'),
        'USER': env.str('POSTGRES_USER'),
        'PASSWORD': env.str('POSTGRES_PASSWORD'),
        'HOST': env.str('DB_HOST'),
        'PORT': env.int('DB_PORT', 5432),
    },
}
