from .xlsxReader import read_excel_file
from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from Client.models import DailyFile, UploadedFile
from django.contrib import messages

@login_required
def upload_page(request):
    return render(request, 'fileIO/upload_daily.html')  # upload.html şablonunu yükler

def upload_file(request):
    if request.method == 'POST' and request.FILES['file']:
        excel_file = request.FILES['file']
        print("ilk ")
        # Dosyayı modele kaydet
        uploaded_file = DailyFile(file=excel_file)
        uploaded_file.save()

        # Excel dosyasını oku
        
        df = read_excel_file(excel_file)

        # Sütun adları ve satırları JSON'a dönüştür
        headers = list(df.columns)
        rows = df.values.tolist()

        # JSON yanıt döndür
        messages.success(request, "Dosya başarıyla yüklendi.")
        return redirect('upload_page')
        # return JsonResponse({"headers": headers, "rows": rows})

    return JsonResponse({"error": "Dosya yüklenemedi."}, status=400)



