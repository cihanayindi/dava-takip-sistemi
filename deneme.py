
bildirim_listesi = [] # bu liste veritabanından gelen liste gibi düşünelim
bildirim_listesi = [
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

# Öncelik sıralaması
priority_order = {"Kırmızı": 1, "Sarı": 2, "Mavi": 3}

# Sıralama işlemi
sıralı_bildirimler = sorted(
    bildirim_listesi,
    key=lambda x: (priority_order[x["priority"]], x["is_read"])
)

# Sonuçları ters çevirip is_read'e göre sıralama
sıralı_bildirimler = sorted(
    sıralı_bildirimler,
    key=lambda x: (x["is_read"])
)

# Sıralı sonuçları yazdırma
for bildirim in sıralı_bildirimler:
    print(bildirim)



notifications = bildirim_listesi

