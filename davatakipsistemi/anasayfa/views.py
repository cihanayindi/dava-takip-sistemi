from django.shortcuts import render
from django.http.response import HttpResponse
from Client.models import Case
from django.contrib.auth import login
from django.contrib.auth.models import User
import datetime
import os.path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Create your views here.

from django.core.paginator import Paginator
from django.shortcuts import render

def index(request):
    # Bir kullanıcı objesi oluştur veya mevcut kullanıcıyı al
    test_user, created = User.objects.get_or_create(username="your_test_username")
    
    # Giriş yapmış gibi ayarla
    login(request, test_user)
    cases = Case.objects.all().order_by('case_number')  # Order by latest cases
    paginator = Paginator(cases, 3)  # Show 10 cases per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Google Calendar API ayarları
    SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]
    creds = None
    events = []
    
    token_path = os.path.join(os.path.dirname(__file__), "token.json")
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)


    if creds:
        try:
            service = build("calendar", "v3", credentials=creds)
            now = datetime.datetime.utcnow().isoformat() + "Z"  # UTC formatında şu anki zaman
            events_result = service.events().list(
                calendarId="primary",
                timeMin=now,
                maxResults=10,
                singleEvents=True,
                orderBy="startTime",
            ).execute()
            events = events_result.get("items", [])
            
        except HttpError as error:
            print(f"Google Calendar API Hatası: {error}")

    # Hem case verilerini hem de takvim etkinliklerini şablona gönder
    return render(request, "anasayfa/index.html", {"page_obj": page_obj, "events": events})


# def index(request):

#     cases = Case.objects.all()  # Veritabanından tüm dava kayıtlarını çekiyoruz
#     for case in cases:
#         print(case.case_number)
#     return render(request, 'anasayfa/index.html', {'cases': cases})

def muvekkildetay(request, id):
    return render(request, "anasayfa/muvekkildetay.html", {
        "id" : id
    })