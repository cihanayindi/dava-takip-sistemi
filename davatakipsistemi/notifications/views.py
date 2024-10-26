from django.shortcuts import render

def notification_list(request):
    # Burada bildirimleri elle tanımlıyoruz

    notifications = [
    {
        "id": 1,
        "url": "https://example.com/acil-dava",
        "message": "Yeni bir acil dava eklendi.",
        "priority": "Kırmızı",  # Acil
        "is_read": False
    },
    {
        "id": 2,
        "url": "https://example.com/original-dava",
        "message": "Müvekkil bilgileri güncellendi.",
        "priority": "Sarı",  # Ortalama
        "is_read": False
    },
    {
        "id": 3,
        "url": "",  # Tıklanmayacak, boş
        "message": "Davanın duruşma tarihi değiştirildi.",
        "priority": "Mavi",  # Acil değil
        "is_read": True
    },
    {
        "id": 4,
        "url": "https://example.com/bildirim-4",
        "message": "Önemli bir bildirim: Lütfen kontrol edin.",
        "priority": "Kırmızı",  # Acil
        "is_read": False
    },
    {
        "id": 5,
        "url": "https://example.com/bildirim-5",
        "message": "Yeni bir mesajınız var.",
        "priority": "Sarı",  # Ortalama
        "is_read": True
    }
]
    return render(request, 'notifications/notifications.html', {'notifications': notifications})
