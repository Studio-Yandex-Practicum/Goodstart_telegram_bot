from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from core.utils import send_registration_email

urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        'registration/',
        include('potential_user.urls'),
        name='registration',
    ),
    path('registration_mail/',
        send_registration_email,
        name='send-registration-email',
    ),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT,
    )
