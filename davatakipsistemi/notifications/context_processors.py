def notification_processor(request): # buraya veritabanından çekilecek bildirimler aşağıdaki gibi sıra sıra girilebilir

    bildirim_listesi = [ # bu liste veritabanından gelen liste gibi düşünelim
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

    def oncelik_siralamasi_yapma(bildirim_listesi):   
        # Öncelik sıralaması
        priority_order = {"Kırmızı": 1, "Sarı": 2, "Mavi": 3}

        # Sıralama işlemi
        bildirim_listesi.sort(key=lambda x: (priority_order[x["priority"]], x["is_read"]))

        return bildirim_listesi
    
    notifications = oncelik_siralamasi_yapma(bildirim_listesi)
    
    return {'notifications': notifications}
