from django.contrib import admin
from django.urls import path, include


from core.utils import send_registration_email

urlpatterns = [
    path('admin/', admin.site.urls),
    path('registration/',
        include('potential_user.urls'),
        name='registration',
    ),
    path('registration_mail/',
        send_registration_email,
        name='send-registration-email',
    ),
]
