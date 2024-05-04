import os

from django.core.asgi import get_asgi_application

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "core.config.settings_dev",
)  # настройки для разработки

application = get_asgi_application()
