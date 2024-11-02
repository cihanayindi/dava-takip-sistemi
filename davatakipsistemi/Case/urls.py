from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('',views.addCase, name='case'),
    path('add_case/',views.addCase, name='add_case'),
    path("<int:id>", views.showCaseDetail,name='show_case_detail'),
    path('case_list/', views.showCaseList, name='case_list'),
    # path('', login_required(views.case, login_url='/auth/login/'), name='case'),
]
