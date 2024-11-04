from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from Client.models import DailyFile
from django.views.decorators.csrf import csrf_exempt

@login_required
def upload_page(request):
    return render(request, 'fileIO/upload_daily.html')  # upload_daily.html şablonunu yükler

@csrf_exempt
@login_required
def upload_file(request):
    if request.method == 'POST':
        files = request.FILES.getlist('files')
        saved_files = []
        
        for excel_file in files:
            uploaded_file = DailyFile(file=excel_file)
            uploaded_file.save()
            saved_files.append(uploaded_file.file.name)

        return JsonResponse({"message": "Dosyalar başarıyla yüklendi.", "files": saved_files})

    return JsonResponse({"error": "Dosya yüklenemedi."}, status=400)
