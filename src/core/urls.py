from django.contrib import admin
from django.urls import path

from .views import send_greeting_email

urlpatterns = [
    path('admin/', admin.site.urls),
    # TODO: убрать после реализации функционала
    path('mail/', send_greeting_email, name='send-email',)
]
