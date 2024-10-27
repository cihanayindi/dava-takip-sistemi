
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.urls import reverse
from .xlsxReader import read_excel_file
# Geçici olarak veriyi saklamak için
excel_data = None

def upload_file(request):
    global excel_data
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        print(file)
        try:
            # Excel dosyasını DataFrame olarak oku
            data = read_excel_file(file)
            excel_data = data.to_dict(orient="records")  # Satır satır JSON formatına dönüştür
            return redirect(reverse('view_excel_data'))
       
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    return render(request, 'fileIO/upload.html')

def view_excel_data(request):
    global excel_data
    return render(request, 'fileIO/view_data.html', {"data": excel_data})
