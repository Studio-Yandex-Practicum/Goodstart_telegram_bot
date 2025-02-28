from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        'registration/',
        include('potential_user.urls'),
        name='registration',
    ),
    path(
        'schedule/',
        include('schooling.urls'),
        name='schedule',
    ),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT)
