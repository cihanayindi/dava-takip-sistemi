from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('get_notifications/', views.get_notifications, name='get_notifications'),
]
