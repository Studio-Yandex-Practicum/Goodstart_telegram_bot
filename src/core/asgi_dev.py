import os

from django.core.asgi import get_asgi_application

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'core.config.settings_for_dev',
)  # настройки для разработки

django_asgi_app = get_asgi_application()


async def application(scope, receive, send):
    """ASGI application to handle incoming ASGI events."""
    from bot.bot_interface import Bot
    if scope['type'] == 'lifespan':
        while True:
            message = await receive()
            if message['type'] == 'lifespan.startup':
                await send({'type': 'lifespan.startup.complete'})
            elif message['type'] == 'lifespan.shutdown':
                Bot().stop()
                await send({'type': 'lifespan.shutdown.complete'})
                return
    else:
        await django_asgi_app(scope, receive, send)
