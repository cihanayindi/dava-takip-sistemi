from django.shortcuts import render, redirect
from django.http import HttpResponse

def client(request):
    return render(request, "Client/client.html")

def muvvekil_ekle(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        tc_no = request.POST.get('tc_no')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        address = request.POST.get('address')
        
        # Burada verileri kaydetme işlemleri yapılabilir
        
        return redirect('success_page')  # Başarılı bir işlem sonrası yönlendirme
    return render(request, 'client/addclient.html')
