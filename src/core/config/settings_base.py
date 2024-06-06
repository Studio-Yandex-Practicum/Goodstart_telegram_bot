import os
from pathlib import Path

import environ
from django.utils.translation import gettext_lazy as _

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ROOT_DIR = BASE_DIR.parent
environ.Env.read_env(os.path.join(ROOT_DIR, '.env'))
env = environ.Env()


STATIC_ROOT = os.path.join(ROOT_DIR, 'static/')

DEFAULT = 'some_default_key'

SECRET_KEY = env('SECRET_KEY', default=DEFAULT)

TELEGRAM_TOKEN = env('TELEGRAM_TOKEN')

ALLOWED_HOSTS = ['*']

DEFAULT_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

LOCAL_APPS = [
    'bot.apps.BotConfig',
    'potential_user.apps.PotentialUserConfig',
    'admin_user.apps.AdminUserConfig',
    'schooling.apps.SchoolingConfig',
]

EXTERNAL_APPS = [
    'material',
    'material.admin',
    'phonenumber_field',
    'django_bootstrap5',
]

INSTALLED_APPS = DEFAULT_APPS + EXTERNAL_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

AUTH_USER_MODEL = 'admin_user.Administrator'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

STATIC_ROOT = BASE_DIR / 'static'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

PHONENUMBER_DEFAULT_REGION = 'RU'

# Конфигурация электронной почты
# По умолчанию, для удобства тестирования во время разработки, все письма выводятся в консоль.
# Для отправки реальных писем
# EMAIL_BACKEND в .env должен быть установлен в 'django.core.mail.backends.smtp.EmailBackend'
# Ниже приведены настройки по умолчанию, использующие переменные окружения.
EMAIL_BACKEND = env.str(
    'EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend',
)
EMAIL_TEMPLATE_NAME = 'emailing/greeting_email.html'
EMAIL_HOST = env.str('EMAIL_HOST', default='smtp.yandex.ru')
try:
    EMAIL_PORT = env.int('EMAIL_PORT', default=456)
except ValueError:
    EMAIL_PORT = 465
EMAIL_HOST_USER = env.str('EMAIL_ACCOUNT', default='example@yandex.ru')
EMAIL_HOST_PASSWORD = env.str('EMAIL_PASSWORD', default='password')
EMAIL_TIMEOUT = 5
EMAIL_USE_SSL = True
DEFAULT_RECEIVER = env.str('DEFAULT_EMAIL_ADDRESS', default='NOT_SET')

BASE_URL = os.getenv('BASE_URL', 'http://127.0.0.1:8000')

MATERIAL_ADMIN_SITE = {
    'HEADER':  _('GoodStart школа'),  # Admin site header
    'TITLE':  _('Администрирование'),  # Admin site title
    'SHOW_THEMES':  True,  # Show default admin themes button
    'NAVBAR_REVERSE': True,  # Hide side navbar by default
    'SHOW_COUNTS': True,  # Show instances counts for each model
}
PERSISTENCE_DIR = ROOT_DIR / 'persistence_data'
PERSISTENCE_PATH = PERSISTENCE_DIR / 'persistence_file'
