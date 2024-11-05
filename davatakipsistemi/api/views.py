from django.shortcuts import render
from django.http import JsonResponse
from Client.models import Notification

# Create your views here.

def get_notifications(request):
    # Fetch notifications from the database
    notifications = Notification.objects.all().filter(read = False)
    
    # Serialize notifications
    notifications_data = [
        {
            'id': notification.id,
            'message': notification.text,
            'url': notification.link,
            'is_read': notification.read,
            'priority': notification.priority,
            'created_at': notification.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        }
        for notification in notifications
    ]
    return JsonResponse(notifications_data, safe=False)



