"""Settings for development."""

from core.config.settings_base import *  # noqa

DEBUG = env('DEBUG')

# WARNING!!!
# You will probably need to make some minor changes to the `.env` file.
# Pull variable names have been changed for better readability.

DATABASES = {
    'default': {
        'ENGINE': env.str(
            'DB_ENGINE',
            'django.db.backends.postgresql_psycopg2',
        ),
        'NAME': env.str('POSTGRES_DB', 'postgres_db'),
        'USER': env.str('POSTGRES_USER', 'postgres'),
        'PASSWORD': env.str('POSTGRES_PASSWORD', 'postgres'),
        'HOST': env.str('DB_HOST', 'localhost'),
        'PORT': env.int('DB_PORT', 5432),
    },
}
