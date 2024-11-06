from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required
# http://127.0.0.1:8000/ => anasayfa
# http://127.0.0.1:8000/index => anasayfa
# http://127.0.0.1:8000/muvekkildetay/1 => 1. müvekkil 

urlpatterns = [
    path("", views.index, name='anasayfa'),
    path("index", views.index, name='anasayfa'),
    path('search/', views.search_cases_clients, name='search_cases_clients'),
    # path("", login_required(views.index, login_url='/auth/login/'), name='anasayfa'),
    # path("index", login_required(views.index, login_url='/auth/login/'), name='anasayfa'),
    # path("muvekkildetay/<int:id>", views.muvekkildetay)
]