import os
from pathlib import Path

import environ


BASE_DIR = Path(__file__).resolve().parent.parent.parent
ROOT_DIR = BASE_DIR.parent
environ.Env.read_env(os.path.join(ROOT_DIR, '.env'))
env = environ.Env()


STATIC_ROOT = os.path.join(ROOT_DIR, 'static/')

DEFAULT = 'some_default_key'

SECRET_KEY = env('SECRET_KEY', default=DEFAULT)

TELEGRAM_TOKEN = env('TELEGRAM_TOKEN')

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['http://127.0.0.1:8000'])

CSRF_TRUSTED_ORIGINS = env.list('CSRF_TRUSTED_ORIGINS', default=['http://127.0.0.1:8000'])


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
    'jazzmin',
    'django.contrib.admin',
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
STATICFILES_DIRS = [
    BASE_DIR / 'staticfiles',
    BASE_DIR / 'static',
]
STATIC_ROOT = ROOT_DIR / 'static'

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
EMAIL_PORT = env.int('EMAIL_PORT', default=465)
EMAIL_HOST_USER = env.str('EMAIL_HOST_USER', default='example@yandex.ru')
EMAIL_HOST_PASSWORD = env.str('EMAIL_HOST_PASSWORD', default='password')
EMAIL_TIMEOUT = 5
EMAIL_USE_SSL = env.bool('EMAIL_USE_SSL', default=True)
DEFAULT_RECEIVER = env.str('DEFAULT_EMAIL_ADDRESS', default='NOT_SET')

BASE_URL = os.getenv('BASE_URL', 'http://127.0.0.1:8000')

JAZZMIN_SETTINGS = {
    'site_title': 'GoodStart Admin',
    'site_header': 'GoodStart',
    'welcome_sign': 'Добро пожаловать в панель администратора!',
    'site_brand': 'GoodStart Admin',
    'show_ui_builder': False,
}

JAZZMIN_UI_TWEAKS = {
    'accent': 'accent-primary',
    'navbar': 'navbar-white navbar-light',
    'sidebar': 'sidebar-dark-primary',
    'theme': 'minty',
    'button_classes': {
        'primary': 'btn-outline-primary',
        'secondary': 'btn-outline-secondary',
        'info': 'btn-info',
        'warning': 'btn-warning',
        'danger': 'btn-danger',
        'success': 'btn-success',
    },

    'custom_css': 'jazzmin/css/main.css',
}
