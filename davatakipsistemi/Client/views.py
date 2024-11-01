from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from .models import Client  # Client modelini içe aktarın
from decimal import Decimal  # Decimal alanları için gerekli

def addClient(request):
    if request.method == 'POST':
        # Formdan gelen verileri alıyoruz
        name = request.POST.get('first_name')
        surname = request.POST.get('last_name')
        tc_no = request.POST.get('tc_no')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        address = request.POST.get('address')
        
        # Diğer alanlar (varsa formdan alınabilir, sabit bir değer atanabilir veya eklenmeyebilir)
        agreement_amount = Decimal(request.POST.get('agreement_amount', '0.00'))  # Anlaşma miktarı
        amount_received = Decimal(request.POST.get('amount_received', '0.00'))  # Alınan miktar
        remaining_balance = agreement_amount - amount_received  # Kalan bakiye
        file_expenses = Decimal(request.POST.get('file_expenses', '0.00'))  # Dosya masrafları
        
        # Client nesnesi oluşturuluyor

        existing_client = Client.objects.filter(tc=tc_no).exists()
        
        if existing_client:
            # Hata mesajı veya yönlendirme yapılabilir
            messages.warning(request, "Bu müşteri zaten kayıtlı.")
            return redirect('add_client')  # Geri sayfaya yönlendirir.
        else:
            client = Client(
            tc=tc_no,
            name=name,
            surname=surname,
            address=address,
            phone=phone,
            email=email,
            agreement_amount=agreement_amount,
            amount_received=amount_received,
            remaining_balance=remaining_balance,
            file_expenses=file_expenses,
            files="",  
            notes="",)
        
            # Kayıt ekleme işlemi
            client.save()
            # Başarılı bir işlem sonrası yönlendirme
            return redirect(f'/client/{client.id}')
    
    # GET isteklerinde form sayfasını render ediyoruz
    else:
        return render(request, 'client/add_client.html')

def showClientDetail(request, id):
    # ID ile Client nesnesini al
    client = get_object_or_404(Client, id=id)
    
    # Client nesnesini template'e gönder
    return render(request, "Client/client.html", {
        "client": client  # Client nesnesini gönderiyoruz
    })
