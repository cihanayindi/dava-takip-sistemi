from Client.models import Notification # Bildirim modelinin yolu
from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse


def add_notification():

    # Örnek bildirim verileri ekle
    Notification.objects.create(
        text='Yeni bir dava kaydedildi: "Örnek Davası".',
        priority=3,  # Yüksek öncelik
        link='https://example.com/dava/1',
    )

    Notification.objects.create(
        text='Davaya itiraz edildi: "Örnek Davası".',
        priority=2,  # Orta öncelik
        link='https://example.com/dava/1/itiraz',
    )

    Notification.objects.create(
        text='Dava duruşması tarihi belirlendi: "Örnek Davası", 15 Kasım 2024.',
        priority=3,  # Yüksek öncelik
        link='https://example.com/dava/1/durusma',
    )

    Notification.objects.create(
        text='Müşteri ile toplantı planlandı: "Örnek Davası".',
        priority=1,  # Düşük öncelik
        link='https://example.com/dava/1/toplanti',
    )

    Notification.objects.create(
        text='Davadan geri çekilme talebi alındı: "Örnek Davası".',
        priority=2,  # Orta öncelik
        link='https://example.com/dava/1/geri-cekilme',
    )

    Notification.objects.create(
        text='Dava dosyası güncellendi: "Örnek Davası".',
        priority=1,  # Düşük öncelik
        link='https://example.com/dava/1/dosyaguncelleme',
    )

    Notification.objects.create(
        text='Mahkeme kararı çıktı: "Örnek Davası".',
        priority=3,  # Yüksek öncelik
        link='https://example.com/dava/1/mahkeme-karari',
    )

    Notification.objects.create(
        text='Yeni kanun değişikliği hakkında bilgi: "Örnek Davası".',
        priority=2,  # Orta öncelik
        link='https://example.com/dava/1/kanun-degisikligi',
    )

    Notification.objects.create(
        text='Davada uzman görüşü alındı: "Örnek Davası".',
        priority=2,  # Orta öncelik
        link='https://example.com/dava/1/uzman-gorusu',
    )

    Notification.objects.create(
        text='Müvekkil ile görüşme tamamlandı: "Örnek Davası".',
        priority=1,  # Düşük öncelik
        link='https://example.com/dava/1/muvekkil-gorusme',
    )

def notification_list(request):
    """
    View to display the list of notifications.
    """
    # Tüm bildirimleri al
    # add_notification()
    notifications = Notification.objects.all()
    context = {
        'notifications': notifications,
    }
    return render(request, 'notifications/notifications.html', context)

def notification_delete(request, id):
    """
    View to delete a specific notification.
    """
    notification = get_object_or_404(Notification, id=id)
    notification.delete()
    return redirect('notification_list')