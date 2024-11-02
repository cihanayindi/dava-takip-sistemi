from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from .models import Client, Case  # Client modelini içe aktarın
from decimal import Decimal  # Decimal alanları için gerekli
from datetime import date

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
    casesForClient = Case.objects.filter(client_id = id)
    
    context = {
        "client": client,  # Client nesnesini gönderiyoruz
        "casesForClient" : casesForClient,
    }

    # Client nesnesini template'e gönder
    return render(request, "Client/client.html", context)

from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Client

def showClientList(request):
    # Sayfa başına gösterilecek öğe sayısını al
    per_page = request.GET.get('per_page', 10)
    
    # Sıralama parametrelerini al (default olarak name alanına göre sırala)
    sort_by = request.GET.get('sort_by', 'name')
    sort_order = request.GET.get('sort_order', 'asc')
    if sort_order == 'desc':
        sort_by = '-' + sort_by

    # Veritabanından Client verilerini çek ve sırala
    client_list = Client.objects.all().order_by(sort_by)
    
    # Sayfalama işlemi
    paginator = Paginator(client_list, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'per_page': per_page,
        'sort_order': sort_order,
        'sort_by': sort_by,
    }
    return render(request, "Client/client_list.html", context)


def addSampleClients(request):
    # Örnek müvekkil verisi ekle
    sample_clients = [
        {
            "tc": "12345678901",
            "name": "Ahmet",
            "surname": "Yılmaz",
            "address": "İstanbul, Türkiye",
            "phone": "05001234567",
            "email": "ahmet@example.com",
            "agreement_amount": Decimal("10000.00"),
            "amount_received": Decimal("5000.00"),
            "remaining_balance": Decimal("5000.00"),
            "file_expenses": Decimal("200.00"),
            "last_sms_date": date(2023, 10, 1),
            "files": "Dosya1, Dosya2",
            "notes": "Önemli not."
        },
        {
            "tc": "98765432109",
            "name": "Mehmet",
            "surname": "Demir",
            "address": "Ankara, Türkiye",
            "phone": "05007654321",
            "email": "mehmet@example.com",
            "agreement_amount": Decimal("15000.00"),
            "amount_received": Decimal("7000.00"),
            "remaining_balance": Decimal("8000.00"),
            "file_expenses": Decimal("300.00"),
            "last_sms_date": date(2023, 9, 15),
            "files": "Dosya3, Dosya4",
            "notes": "Belge eklenecek."
        },
        # Diğer örnek veriler
        {
            "tc": "11223344556",
            "name": "Ayşe",
            "surname": "Çelik",
            "address": "İzmir, Türkiye",
            "phone": "05553334455",
            "email": "ayse@example.com",
            "agreement_amount": Decimal("20000.00"),
            "amount_received": Decimal("15000.00"),
            "remaining_balance": Decimal("5000.00"),
            "file_expenses": Decimal("500.00"),
            "last_sms_date": date(2023, 10, 20),
            "files": "Dosya5, Dosya6",
            "notes": "SMS gönderilecek."
        },
        {
            "tc": "22334455667",
            "name": "Fatma",
            "surname": "Şahin",
            "address": "Bursa, Türkiye",
            "phone": "05331234567",
            "email": "fatma@example.com",
            "agreement_amount": Decimal("8000.00"),
            "amount_received": Decimal("4000.00"),
            "remaining_balance": Decimal("4000.00"),
            "file_expenses": Decimal("100.00"),
            "last_sms_date": date(2023, 9, 30),
            "files": "Dosya7",
            "notes": "Dava bilgisi güncellenecek."
        },
        {
            "tc": "33445566778",
            "name": "Emre",
            "surname": "Kara",
            "address": "Antalya, Türkiye",
            "phone": "05431234567",
            "email": "emre@example.com",
            "agreement_amount": Decimal("12000.00"),
            "amount_received": Decimal("6000.00"),
            "remaining_balance": Decimal("6000.00"),
            "file_expenses": Decimal("150.00"),
            "last_sms_date": date(2023, 9, 10),
            "files": "Dosya8",
            "notes": "Yeni dosya açılacak."
        },
        # Diğer 5 örnek müvekkil verisi aynı yapıda eklenebilir.
    ]

    for client_data in sample_clients:
        Client.objects.create(**client_data)
