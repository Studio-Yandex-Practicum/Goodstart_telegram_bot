"""Settings for production."""

from core.config.settings_base import *  # noqa

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': env.str(
            'DB_ENGINE',
            'django.db.backends.postgresql_psycopg2',
        ),
        'NAME': env.str('DB_NAME', 'postgres_db'),
        'USER': env.str('DB_USERNAME', 'postgres'),
        'PASSWORD': env.str('DB_PASSWORD', 'postgres'),
        'HOST': env.str('DB_HOST', 'localhost'),
        'PORT': env.int('DB_PORT', 5432),
    },
}
