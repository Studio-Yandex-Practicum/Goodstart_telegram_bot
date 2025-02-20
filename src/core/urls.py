from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from schooling import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        'registration/',
        include('potential_user.urls'),
        name='registration',
    ),
    path(
        'schedule/',
        include('schooling.urls'),
        name='schedule',
    ),
    path('payment/',
         views.payment_view,
         name='payment_view'),
    path('payment_summary/<int:lessons>/',
         views.payment_summary_view,
         name='payment_summary'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT)
