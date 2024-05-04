import os

from django.core.asgi import get_asgi_application

os.environ.setdefault(
<<<<<<< HEAD
    'DJANGO_SETTINGS_MODULE', 'core.config.settings_prod'
=======
    "DJANGO_SETTINGS_MODULE",
    "core.config.settings_prod",
>>>>>>> dev
)  # настройки для сервера

application = get_asgi_application()
