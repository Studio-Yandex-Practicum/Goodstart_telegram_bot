from django.urls import path

from potential_user.views import RegistrationCreateView, registration_success

app_name = 'registration'

urlpatterns = [
    path('',
         RegistrationCreateView.as_view(),
         name='registration'),
    path('registration_success/',
         registration_success,
         name='registration_success'),
]
