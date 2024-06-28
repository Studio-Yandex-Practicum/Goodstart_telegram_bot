from django.urls import path

from schooling.views import (
    schedule_page, details_schedule_page, cancel_lesson,
    change_datetime_lesson, lesson_change_success, lesson_cancel_success,
)

app_name = 'schedule'

urlpatterns = [
    path('<int:id>/', schedule_page, name='schedule'),
    path(
        '<int:id>/<int:lesson_id>/',
        details_schedule_page,
        name='details_schedule',
    ),
    path(
        '<int:id>/<int:lesson_id>/change-datetime-lesson/',
        change_datetime_lesson,
        name='change_datetime_lesson',
    ),
    path(
        '<int:id>/<int:lesson_id>/cancel-lesson/',
        cancel_lesson,
        name='cancel_lesson',
    ),
    path('lesson_change_success/',
         lesson_change_success,
         name='lesson_change_success',
    ),
    path('lesson_cancel_success/',
         lesson_cancel_success,
         name='lesson_cancel_success',
    ),
]
