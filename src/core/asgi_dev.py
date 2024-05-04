import os

from django.core.asgi import get_asgi_application

os.environ.setdefault(
<<<<<<< HEAD
    'DJANGO_SETTINGS_MODULE', 'core.config.settings_dev'
=======
    "DJANGO_SETTINGS_MODULE",
    "core.config.settings_dev",
>>>>>>> dev
)  # настройки для разработки

application = get_asgi_application()
