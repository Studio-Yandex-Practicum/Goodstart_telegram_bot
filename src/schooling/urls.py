from django.urls import path

from schooling.views import schedule_page

app_name = 'schedule'

urlpatterns = [
    path('<int:id>/', schedule_page, name='schedule'),
]
