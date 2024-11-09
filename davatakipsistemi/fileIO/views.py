from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from Client.models import DailyFile
from django.views.decorators.csrf import csrf_exempt
from .xlsxReader import read_excel_file
import pandas as pd
from Client.models import Case,ProcessTypes


def add_process_type():
    df =read_excel_file("C:/Users/suakb/supi/bionluk/dava-takip-sistemi/excelIcerikleri/işlem türleri avukat1.xlsx")
    liste = df.values.tolist()
    for row in liste:
        process_type = row[1]
        deadline = row[2]
        priority = row[3]
        new_process_type = ProcessTypes(file_type = 'safahat',process_type=process_type, deadline=deadline, priority=priority)
        new_process_type.save()

@login_required
def upload_page(request):
    # add_process_type()
    return render(request, 'fileIO/upload_daily.html')  # upload_daily.html şablonunu yükler

@csrf_exempt
@login_required
def upload_file(request):
    if request.method == 'POST':
        files = request.FILES.getlist('files')
        file_types = request.POST.getlist('file_types')  # Dosya türlerini alıyoruz
        saved_files = []

        for index, excel_file in enumerate(files):
            file_type = file_types[index]  # Dosya tipini al
            yapilan_kayit = 0
            df = read_excel_file(excel_file)
            if file_type == 'safahat':
                df =df.drop('No',axis=1)
                basliklar = df.columns.tolist()
                liste = df.values.tolist()
                for row in liste:
                    print(row)
                    if  "Dosya Türü" in basliklar:
                        islem_yapan_birim = row[0]
                        dosya_no = row[1]
                        dosya_turu = row[2]
                        islem_turu = row[3]
                        karar_tarihi = row[4]
                        aciklama = row[5]
                        
                    else:
                        islem_yapan_birim = row[0]
                        dosya_no = row[1]
                        karar_tarihi = row[2]
                        islem_turu = row[3]
                        aciklama = row[4]
                    print(islem_turu)                      
                    current_process = ProcessTypes.objects.filter(process_type=islem_turu)      
                    if current_process:
                        current_process = current_process[0]
                        print(current_process, current_process.deadline)              
                    # related_case = Case.objects.get(court = islem_yapan_birim,case_number=dosya_no)


            elif file_type == 'tebligat':
                pass
            elif file_type == 'duruşma':
                pass
            print(yapilan_kayit)
            print(excel_file,file_type)
            
            # uploaded_file = DailyFile(file=excel_file, file_type=file_type)
            # uploaded_file.save()
            # saved_files.append(uploaded_file.file.name)

        return JsonResponse({"message": "Dosyalar başarıyla yüklendi.", "files": saved_files})

    return JsonResponse({"error": "Dosya yüklenemedi."}, status=400)
