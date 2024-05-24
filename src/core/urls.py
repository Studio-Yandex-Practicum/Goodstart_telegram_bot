from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from core.views import send_greeting_email

urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        'registration/',
        include('potential_user.urls'),
        name='registration',
        ),
    # TODO: убрать после реализации функционала
    path('mail/', send_greeting_email, name='send-email'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
