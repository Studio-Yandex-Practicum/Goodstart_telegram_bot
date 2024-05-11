from django.urls import path

from .views import RegistrationCreateView, TemplateIndex

app_name = 'registration'

urlpatterns = [
    path('',
         RegistrationCreateView.as_view(),
         name='registration'),
    # Временная индексная страница
    path('', TemplateIndex.as_view(), name='index'),
]
