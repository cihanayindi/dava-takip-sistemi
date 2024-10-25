from django.urls import path
from . import views
# http://127.0.0.1:8000/ => anasayfa
# http://127.0.0.1:8000/index => anasayfa
# http://127.0.0.1:8000/muvekkildetay/1 => 1. müvekkil 

urlpatterns = [
    path("", views.index),
    path("index", views.index),
    path("muvekkildetay/<int:id>", views.muvekkildetay)
]