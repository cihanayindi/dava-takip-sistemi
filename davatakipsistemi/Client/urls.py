from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views.addClient, name='client'),
    path('add_client/', views.addClient, name='add_client'),
    path("<int:id>", views.showClientDetail,name='show_client_detail'),
    # path('', login_required(views.client, login_url='/auth/login/'), name='client'),
    # path('addclient/', login_required(views.muvekkilEkle, login_url='/auth/login/'), name='muvekkilekle'),
]
