from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('registration/',
        include('potential_user.urls'),
        name='registration',
    ),
]
