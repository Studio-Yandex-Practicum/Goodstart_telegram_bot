from django.urls import path

from .views import RegistrationCreateView

app_name = 'registration'

urlpatterns = [
    path('',
         RegistrationCreateView.as_view(),
         name='registration'),
]
