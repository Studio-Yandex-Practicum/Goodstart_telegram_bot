from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from schooling.views import (schedule_page, details_schedule_page,
                             edit_homework, delete_homework_image,
                             delete_homework_file)


app_name = 'schedule'

urlpatterns = [
    path('<int:id>/', schedule_page, name='schedule'),
    path(
        '<int:id>/<int:lesson_id>/',
        details_schedule_page,
        name='details_schedule',
    ),
    path(
        '<int:id>/<int:lesson_id>/edit/',
        edit_homework,
        name='edit_homework',
    ),
    path(
        '<int:id>/<int:lesson_id>/delete_image/<int:image_id>/',
        delete_homework_image,
        name='delete_homework_image',
    ),
    path(
        '<int:id>/<int:lesson_id>/delete_file/<int:file_id>/',
        delete_homework_file,
        name='delete_homework_file',
    ),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT,
    )
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
