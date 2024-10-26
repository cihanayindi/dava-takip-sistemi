# views.py
from django.shortcuts import render
from django.http import JsonResponse
from .forms import UploadFileForm
import pandas as pd
import io

def upload_file(request):
    print("request method: ", request.method)
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        try:
            # Excel dosyasını DataFrame olarak oku
            data = pd.read_excel(file)
            # Burada gelen veriyi işleminiz için saklayabilirsiniz
            return JsonResponse({"status": "success", "data": data.to_dict()})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    return render(request, 'fileIO/upload.html')
