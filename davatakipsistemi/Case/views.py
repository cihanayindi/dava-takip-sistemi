from django.shortcuts import render, redirect, get_object_or_404
from Client.models import Case
from Client.models import Client  # Client modelinin yolu
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import date


def addCase(request):
    if request.method == 'POST':
        # Formdan gelen verileri alıyoruz
        client_id = request.POST.get('client')  # Müvekkil ID'si
        case_number = request.POST.get('case_number')
        case_type = request.POST.get('case_type')
        status = request.POST.get('status')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        hearing_date = request.POST.get('hearing_date')
        court = request.POST.get('court')
        description = request.POST.get('description')
        case_file = request.FILES.get('case_file')  # Dosya yükleme

        # Client modelinden müvekkili alıyoruz
        try:
            client = Client.objects.get(id=client_id)  # Müvekkili al
        except Client.DoesNotExist:
            messages.error(request, "Seçilen müvekkil bulunamadı.")
            return redirect('add_case')  # Hata durumunda tekrar ekleme sayfasına yönlendir

        # Dava nesnesi oluştur
        case = Case(
            client=client,
            case_number=case_number,
            case_type=case_type,
            status=status,
            start_date=start_date,
            end_date=end_date,
            hearing_date=hearing_date,
            court=court,
            description=description,
            case_file=case_file,  # Dosya yükleme
        )
        
        # Veritabanına kaydet
        case.save()
        
        messages.success(request, "Dava başarıyla eklendi.")
        return redirect(f'/case/{case.id}')  # Başarılı işlemden sonra yönlendirme

    # GET isteği için form sayfasını render et
    clients = Client.objects.all()  # Tüm müvekkilleri al
    return render(request, "case/add_case.html", {'clients': clients})


def showCaseDetail(request, id):
    case = get_object_or_404(Case, id=id)
    return render(request, "Case/case.html", {"case": case})

def showCaseList(request):
    return render(request, "case/case_list.html")

def addSampleCases(request):
    # Örnek dava verisi ekle
    print("çalıştı")
    sample_cases = [
        {
            "client_id": 1,
            "case_number": "D20231001",
            "case_type": "Criminal",
            "status": "Ongoing",
            "start_date": date(2023, 10, 1),
            "hearing_date": date(2023, 12, 1),
            "court": "İstanbul 2. Ağır Ceza Mahkemesi",
            "description": "Dava ile ilgili detaylı açıklama.",
            "updated_by_id": 1  # User id'si
        },
        {
            "client_id": 3,
            "case_number": "D20231002",
            "case_type": "Civil",
            "status": "Resolved",
            "start_date": date(2023, 8, 15),
            "end_date": date(2023, 10, 20),
            "hearing_date": date(2023, 9, 15),
            "court": "Ankara 1. Asliye Hukuk Mahkemesi",
            "description": "Davanın çözüm süreci tamamlanmıştır.",
            "updated_by_id": 2
        },
        {
            "client_id": 4,
            "case_number": "D20231003",
            "case_type": "Labor",
            "status": "Closed",
            "start_date": date(2023, 7, 10),
            "end_date": date(2023, 9, 25),
            "hearing_date": date(2023, 8, 5),
            "court": "Bursa İş Mahkemesi",
            "description": "İş hukuku davası kapatıldı.",
            "updated_by_id": 1
        },
        {
            "client_id": 5,
            "case_number": "D20231004",
            "case_type": "Family",
            "status": "Ongoing",
            "start_date": date(2023, 9, 1),
            "hearing_date": date(2023, 11, 15),
            "court": "İzmir Aile Mahkemesi",
            "description": "Aile hukuku davası devam ediyor.",
            "updated_by_id": 3
        },
        {
            "client_id": 6,
            "case_number": "D20231005",
            "case_type": "Commercial",
            "status": "Resolved",
            "start_date": date(2023, 6, 1),
            "end_date": date(2023, 9, 10),
            "hearing_date": date(2023, 8, 20),
            "court": "Adana Ticaret Mahkemesi",
            "description": "Ticaret hukuku davası sonuçlandı.",
            "updated_by_id": 2
        },
        {
            "client_id": 7,
            "case_number": "D20231006",
            "case_type": "Criminal",
            "status": "Ongoing",
            "start_date": date(2023, 10, 5),
            "hearing_date": date(2023, 12, 10),
            "court": "Antalya Ağır Ceza Mahkemesi",
            "description": "Ceza davası süreci devam ediyor.",
            "updated_by_id": 1
        },
        {
            "client_id": 1,
            "case_number": "D20231007",
            "case_type": "Civil",
            "status": "Ongoing",
            "start_date": date(2023, 9, 10),
            "hearing_date": date(2023, 11, 1),
            "court": "Konya Asliye Hukuk Mahkemesi",
            "description": "Hukuk davası devam ediyor.",
            "updated_by_id": 3
        },
        {
            "client_id": 3,
            "case_number": "D20231008",
            "case_type": "Labor",
            "status": "Closed",
            "start_date": date(2023, 7, 1),
            "end_date": date(2023, 8, 25),
            "hearing_date": date(2023, 7, 20),
            "court": "Eskişehir İş Mahkemesi",
            "description": "İş davası kapatıldı.",
            "updated_by_id": 2
        },
        {
            "client_id": 5,
            "case_number": "D20231009",
            "case_type": "Family",
            "status": "Resolved",
            "start_date": date(2023, 5, 15),
            "end_date": date(2023, 9, 5),
            "hearing_date": date(2023, 8, 1),
            "court": "Samsun Aile Mahkemesi",
            "description": "Aile davası çözüldü.",
            "updated_by_id": 1
        },
        {
            "client_id": 6,
            "case_number": "D20231010",
            "case_type": "Commercial",
            "status": "Ongoing",
            "start_date": date(2023, 9, 5),
            "hearing_date": date(2023, 12, 1),
            "court": "Kayseri Ticaret Mahkemesi",
            "description": "Ticaret hukuku davası devam ediyor.",
            "updated_by_id": 3
        }
    ]

    for case_data in sample_cases:
        client = Client.objects.get(id=case_data["client_id"])  # Müvekkil nesnesini al
        updated_by = None

        # Foreign key ilişkilerini güncelleyerek Case nesnesini oluştur
        Case.objects.create(
            client=client,
            case_number=case_data["case_number"],
            case_type=case_data["case_type"],
            status=case_data["status"],
            start_date=case_data["start_date"],
            end_date=case_data.get("end_date"),
            hearing_date=case_data.get("hearing_date"),
            court=case_data["court"],
            description=case_data["description"],
            updated_by=updated_by
        )
    
    return render(request, "case/sample_cases_added.html")  # Başarılı ekleme sonrası sayfa render et

