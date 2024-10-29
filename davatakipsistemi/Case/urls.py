from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('',views.addCase, name='case'),
    path('case/add_case/',views.addCase, name='add_case'),

    # path('', login_required(views.case, login_url='/auth/login/'), name='case'),
]
