from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("", views.show_work_list, name='work_list'),
    path("show_work_list/", views.show_work_list, name="work_list"),
]