from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from Client.models import DailyFile
from django.views.decorators.csrf import csrf_exempt
from .xlsxReader import read_excel_file
import pandas as pd
from Client.models import Case,ProcessTypes,CaseProgress,Notification
from datetime import datetime, timedelta





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
    """Dosyaları yükler ve içeriklerine göre işleme alır."""
    if request.method == 'POST':
        files = request.FILES.getlist('files')
        file_types = request.POST.getlist('file_types')
        saved_files = []

        for index, excel_file in enumerate(files):
            file_type = file_types[index]
            df = read_excel_file(excel_file)
            
            if file_type == 'safahat':
                process_safahat_file(df)
            elif file_type == 'tebligat':
                process_tebligat_file(df)
            elif file_type == 'duruşma':
                process_durusma_file(df)

            saved_files.append(excel_file.name)
        
        return JsonResponse({"message": "Dosyalar başarıyla yüklendi.", "files": saved_files})

    return JsonResponse({"error": "Dosya yüklenemedi."}, status=400)


def process_safahat_file(df):
    """Safahat dosyasını işler ve ilgili case progress'leri oluşturur."""
    df = df.drop('No', axis=1)
    basliklar = df.columns.tolist()
    rows = df.values.tolist()

    for row in rows:
        islem_yapan_birim, dosya_no, karar_tarihi, islem_turu, aciklama = extract_safahat_row_data(row, basliklar)
        
        current_process = ProcessTypes.objects.filter(process_type=islem_turu).first()
        if not current_process:
            log_missing_process_type(islem_turu)
            continue
        
        date_obj = datetime.strptime(karar_tarihi, "%d.%m.%Y")
        
        progress_date=date_obj.strftime("%Y-%m-%d")
        progress_text = f"Karar Tarihi : {progress_date}\nİşlem Türü:{islem_turu}\nAçıklama:{aciklama} "
        
        # İşlem türü bulunan case ile ilgili işlemleri yap
        related_case = Case.objects.filter(court=islem_yapan_birim, case_number=dosya_no).first()
        if related_case:
            notification_text=f"Dava Güncellendi:{islem_yapan_birim} - {dosya_no}\n{islem_turu}"
            deadline = date_obj + timedelta(days=current_process.deadline)
            deadline = deadline.strftime("%Y-%m-%d")
            # Mevcut dava güncelleniyor
            create_case_progress(case=related_case, progress_date=progress_date, description=progress_text)    
            create_notification(text=notification_text,
                priority=current_process.priority,
                link=f"/case/{related_case.id}",
                deadline_date=progress_date)
        
        else:
            notification_text=f"Safahat ile Otomatik Yeni Dava Eklendi : {islem_yapan_birim} - {dosya_no}\n{islem_turu}"
            deadline = date_obj + timedelta(days=7)
            deadline = deadline.strftime("%Y-%m-%d")
            # Yeni dava oluşturuluyor
            new_case = create_new_case(islem_yapan_birim, dosya_no)
            create_case_progress(case=new_case, progress_date=progress_date, description=progress_text)    
            
            create_notification(text=notification_text,
                                priority=3,
                                link=f"/case/{new_case.id}",
                                deadline_date=deadline)
            

def process_tebligat_file(df):
    """Tebligat dosyasını işler ve ilgili case progress'leri oluşturur."""
    df = df.drop(['Boyut'], axis=1, errors='ignore')
    rows = df.values.tolist()
    for row in rows:
        gonderen,konu, durum, teslim_tarihi = extract_tebligat_row_data(row)
        
        mahkeme, dosya_no = parse_case_details(konu)

        date_obj = datetime.strptime(teslim_tarihi, "%d.%m.%Y %H:%M")
        progress_date=date_obj.strftime("%Y-%m-%d")
        
        progress_text = f"""Gönderen: {gonderen} Tebligat Durumu : {durum} - Teslim Tarihi : {progress_date}"""
        related_case = Case.objects.filter(court=mahkeme, case_number=dosya_no).first()
        if related_case:
            notification_text = f"Davanıza Tebligat Geldi :{mahkeme}-{dosya_no}"
            deadline = date_obj + timedelta(days=5)
            deadline = deadline.strftime("%Y-%m-%d")
            create_case_progress(case=related_case,
                                 description=progress_text, 
                                 progress_date= progress_date)
            create_notification(text=notification_text, 
                                priority=1, 
                                link=f"/case/{related_case.id}", 
                                deadline_date=deadline)
        else:
            notification_text = f"Tebligat ile Yeni Dava Eklendi, müvekkil ekleyiniz : {mahkeme}-{dosya_no}"
            
            new_case = create_new_case(mahkeme, dosya_no)
            create_case_progress(case=new_case,
                                 description=progress_text,
                                 progress_date=progress_date)
            create_notification(text=notification_text,
                                priority=3,
                                link=f"/case/{new_case.id}" ,
                                deadline_date=progress_date)


def process_durusma_file(df):
    """Duruşma dosyasını işler ve ilgili case progress'leri oluşturur."""
    df = df.drop('İzinli Hakim', axis=1, errors='ignore')
    rows = df.values.tolist()
    
    for row in rows:
        mahkeme, dosya_no, dosya_turu, durusma_tarihi, taraf_bilgi, islem, sonuc = extract_durusma_row_data(row)
        progress_text = generate_progress_text_durusma(durusma_tarihi, dosya_turu, islem, sonuc, taraf_bilgi)
        
        
        # progress_date = format_datetime(durusma_tarihi)
        date_obj = datetime.strptime(durusma_tarihi, "%d.%m.%Y %H:%M:%S")
        progress_date = date_obj.strftime("%Y-%m-%d %H:%M:%S")
        related_case = Case.objects.filter(court=mahkeme, case_number=dosya_no).first()
        
        if related_case:
            notification_text = f"Davanıza Yeni Duruşma Tarihi Eklendi : {mahkeme}-{dosya_no}"
            deadline = date_obj + timedelta(days=5)
            deadline = deadline.strftime("%Y-%m-%d")
            create_case_progress(case=related_case,
                                 description=progress_text, 
                                 progress_date= progress_date)
            create_notification(text=notification_text, 
                                priority=1, 
                                link=f"/case/{new_case.id}", 
                                deadline_date=deadline)
        
        else:
            
            notification_text = f"Duruşma ile Dava Eklendi, müvekkil ekleyiniz : {mahkeme}-{dosya_no}"
            new_case = create_new_case(mahkeme, dosya_no)
            deadline = date_obj + timedelta(days=5)
            deadline = deadline.strftime("%Y-%m-%d")
            
            create_case_progress(case=new_case,
                                 description=progress_text,
                                 progress_date=progress_date)
            create_notification(text=notification_text,
                                priority=3,
                                link=f"/case/{new_case.id}" ,
                                deadline_date=deadline)


def update_case_progress(related_case, islem_turu, aciklama, karar_tarihi):
    """Mevcut dava için ilerleme kaydeder."""
    

def parse_case_details(konu):
    """Konudan mahkeme ve dosya numarasını çıkarır."""
    konu = (konu.split("["))[-1].split("-")
    mahkeme = konu[0].strip()
    dosya_no = konu[-1].replace("]","").strip()
            
    return mahkeme, dosya_no

def extract_safahat_row_data(row, basliklar):
    """Safahat dosyasındaki bir satırdan gerekli veriyi çıkartır."""
    if "Dosya Türü" in basliklar:
        return row[0], row[1], row[4], row[3], row[5]
    else:
        return row[0], row[1], row[2], row[3], row[4] if len(row) > 4 else None

def log_missing_process_type(islem_turu):
    """İşlem türü bulunamadığında log kaydeder."""
    with open("bulunamayan.txt", "a+", encoding="utf-8") as f:
        f.write(islem_turu + "\n")
    print("İşlem türü bulunamadı")

def create_new_case(mahkeme, dosya_no):
    """Yeni dava kaydeder."""
    new_case = Case(court=mahkeme, case_number=dosya_no)
    new_case.save()
    return new_case


def create_case_progress(case, progress_date, description=None):
    """Dava ilerleme kaydeder."""
    case_progress = CaseProgress(case=case, description=description, progress_date=progress_date)
    case_progress.save()


def create_notification(text,priority =3,link=None, deadline_date=None):
    """Yeni bir bildirim oluşturur."""
    notification = Notification(text=text,
                                priority=priority,
                                link=link,
                                deadline_date=deadline_date)
    notification.save()

def generate_progress_text_durusma(durusma_tarihi, dosya_turu, islem, sonuc, taraf_bilgi):
    """Duruşma için ilerleme metni oluşturur."""
    return f"Dava Duruşma Güncellemesi Tarih:{durusma_tarihi}\nDosya Türü: {dosya_turu} - İşlem: {islem} - Sonuç: {sonuc}\nTaraf Bilgisi: {taraf_bilgi}"

def extract_tebligat_row_data(row):
    """Tebligat dosyasındaki bir satırdan gerekli veriyi çıkartır."""
    gonderen = row[0]
    konu = row[1]
    durum = row[2]
    teslim_tarihi = row[3]
    return gonderen, konu, durum, teslim_tarihi

def extract_durusma_row_data(row):
    """Duruşma dosyasındaki bir satırdan gerekli veriyi çıkartır."""
    return row[0], row[1], row[2], row[3], row[4], row[5], row[6]

def format_datetime(date_str):
    """Tarihi ve saati doğru formatta dönüştürür."""
    date_obj = datetime.strptime(date_str, "%d.%m.%Y %H:%M:%S")
    return date_obj.strftime("%Y-%m-%d %H:%M:%S")
