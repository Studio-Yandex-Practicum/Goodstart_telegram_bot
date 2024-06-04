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
    'material',
    'material.admin',
    # 'django.contrib.admin',
    'core.apps.GoodStartAdminConfig',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_bootstrap5',
]

LOCAL_APPS = [
    'bot.apps.BotConfig',
    'potential_user.apps.PotentialUserConfig',
    'admin_user.apps.AdminUserConfig',
    'schooling.apps.SchoolingConfig',
]

EXTERNAL_APPS = ['phonenumber_field']

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
    'HEADER':  _('Административная панель'),  # Admin site header
    'TITLE':  _('Административная панель'),  # Admin site title
    # 'FAVICON':  'base/icons8-favicon-16.png',  # Admin site favicon (path to static should be specified)
    # 'MAIN_BG_COLOR':  'color',  # Admin site main color, css color should be specified
    # 'MAIN_HOVER_COLOR':  'color',  # Admin site main hover color, css color should be specified
    # 'PROFILE_PICTURE':  'font.jpg',  # Admin site profile picture (path to static should be specified)
    # 'PROFILE_BG':  'font.jpg',  # Admin site profile background (path to static should be specified)
    # 'LOGIN_LOGO':  'font.jpg',  # Admin site logo on login page (path to static should be specified)
    # 'LOGOUT_BG':  'font.jpg',  # Admin site background on login/logout pages (path to static should be specified)
    'SHOW_THEMES':  True,  # Show default admin themes button
    # 'TRAY_REVERSE': True,  # Hide object-tools and additional-submit-line by default
    'NAVBAR_REVERSE': True,  # Hide side navbar by default
    'SHOW_COUNTS': True,  # Show instances counts for each model
    # 'APP_ICONS': {  # Set icons for applications(lowercase), including 3rd party apps, {'application_name': 'material_icon_name', ...}
    #     'sites': 'send',
    # },
    # 'MODEL_ICONS': {  # Set icons for models(lowercase), including 3rd party models, {'model_name': 'material_icon_name', ...}
    #     'site': 'contact_mail',
    # }
}
PERSISTENCE_DIR = ROOT_DIR / 'persistence_data'
PERSISTENCE_PATH = PERSISTENCE_DIR / 'persistence_file'
