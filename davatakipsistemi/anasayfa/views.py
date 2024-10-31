from django.shortcuts import render
from django.http.response import HttpResponse
from Client.models import Case
from django.contrib.auth import login
from django.contrib.auth.models import User

# Create your views here.

def index(request):
    # Bir kullanıcı objesi oluştur veya mevcut kullanıcıyı al
    test_user, created = User.objects.get_or_create(username="your_test_username")
    
    # Giriş yapmış gibi ayarla
    login(request, test_user)
    cases = Case.objects.all()  # Veritabanından tüm dava kayıtlarını çekiyoruz
    for case in cases:
        print(case.case_number)
    return render(request, 'anasayfa/index.html', {'cases': cases})

def muvekkildetay(request, id):
    return render(request, "anasayfa/muvekkildetay.html", {
        "id" : id
    })