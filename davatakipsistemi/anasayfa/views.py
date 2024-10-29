from django.shortcuts import render
from django.http.response import HttpResponse
from Client.models import Case
# Create your views here.

def index(request):
    cases = Case.objects.all()  # Veritabanından tüm dava kayıtlarını çekiyoruz
    for case in cases:
        print(case.case_number)
    return render(request, 'anasayfa/index.html', {'cases': cases})

def muvekkildetay(request, id):
    return render(request, "anasayfa/muvekkildetay.html", {
        "id" : id
    })