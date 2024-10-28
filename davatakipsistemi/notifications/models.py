from django.db import models
from django.contrib.auth.models import User

class Notification(models.Model):
    """
    Model to store notifications related to legal cases or clients.

    Attributes:
        id (AutoField): Unique identifier for the notification.
        text (TextField): The notification text.
        priority (IntegerField): Numeric priority level (1 for Low, 2 for Medium, 3 for High).
        link (URLField): Associated link for the notification.
        read (BooleanField): Indicates whether the notification has been read.
        created_at (DateTimeField): Timestamp when the notification was created.
        last_action_date (DateTimeField): Timestamp of the last action taken on the notification.
    """

    id = models.AutoField(primary_key=True)  # Unique identifier
    text = models.TextField()  # Notification text
    priority = models.IntegerField()  # Priority level as a numeric value (1, 2, 3)
    link = models.URLField()  # Link associated with the notification
    read = models.BooleanField(default=False)  # Read status
    created_at = models.DateTimeField(auto_now_add=True)  # Creation timestamp
    last_action_date = models.DateTimeField(auto_now=True)  # Last action timestamp

    class Meta:
        db_table = 'notification'
        ordering = ['-priority', 'read', '-created_at']  # Ordering by priority, read status, and created date

    def __str__(self):
        return f"{self.text} - {self.priority}"
