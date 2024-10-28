from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views.client, name='client'),
    path('addclient/', views.muvekkilEkle, name='muvekkilekle'),
    # path('', login_required(views.client, login_url='/auth/login/'), name='client'),
    # path('addclient/', login_required(views.muvekkilEkle, login_url='/auth/login/'), name='muvekkilekle'),
]
