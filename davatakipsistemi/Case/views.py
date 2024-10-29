from django.shortcuts import render, redirect
from Client.models import Case
from Client.models import Client  # Client modelinin yolu
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, get_object_or_404


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
# Create your views here.
