"""Settings for running tests."""

from core.config.settings_base import *  # noqa

DEBUG = False

DATABASES = {
<<<<<<< HEAD
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
=======
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    },
>>>>>>> dev
}
