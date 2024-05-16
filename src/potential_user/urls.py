from django.urls import path

from potential_user.views import RegistrationCreateView

app_name = 'registration'

urlpatterns = [
    path('',
         RegistrationCreateView.as_view(),
         name='registration'),
]
