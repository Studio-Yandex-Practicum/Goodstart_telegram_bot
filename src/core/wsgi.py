import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.config.settings_dev")  # настройки для разработки
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.config.settings_tests")  # настройки для тестирования
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.config.settings_prod")  # настройки для сервера

application = get_wsgi_application()
