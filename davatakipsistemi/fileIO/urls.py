from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_file, name='upload_file'),
    path('view-data/', views.view_excel_data, name='view_excel_data'),
]
