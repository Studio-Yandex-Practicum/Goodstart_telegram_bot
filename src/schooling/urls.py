from django.urls import path

from schooling.views import schedule_page, details_schedule_page

app_name = 'schedule'

urlpatterns = [
    path('<int:id>/', schedule_page, name='schedule'),
    path(
        '<int:id>/<int:lesson_id>/',
        details_schedule_page,
        name='details_schedule'
    ),
]
