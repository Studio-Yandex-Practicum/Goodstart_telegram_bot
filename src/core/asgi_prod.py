import os

from django.core.asgi import get_asgi_application

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'core.config.settings_for_prod',
)  # настройки для сервера

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
                break
    else:
        await django_asgi_app(scope, receive, send)
