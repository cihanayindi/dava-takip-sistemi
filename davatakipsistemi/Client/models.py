from django.db import models
from django.contrib.auth.models import User
import os


class Client(models.Model):
    """
    Client model to store information about legal clients.

    Attributes:
        id (AutoField): Unique identifier for the client, automatically incremented.
        tc (str): Turkish Identification Number, unique for each client.
        address (str): Address of the client.
        phone (str): Phone number of the client.
        email (str): Email address of the client.
        agreement_amount (Decimal): Amount agreed upon for the new case.
        amount_received (Decimal): Amount received from the client.
        remaining_balance (Decimal): Remaining balance owed by the client.
        file_expenses (Decimal): Expenses related to the client's case files.
        last_sms_date (DateField): Date of the last SMS sent to the client.
        files (str): Files associated with the client.
        created_at (DateTimeField): Timestamp when the client record was created.
        updated_at (DateTimeField): Timestamp when the client record was last updated.
        notes (str): Additional notes about the client.
    """
    
    id = models.AutoField(primary_key=True)  # Otomatik artan ve unique id
    tc = models.CharField(max_length=11, unique=True)  # T.C. Kimlik No
    address = models.TextField()  # Adres
    phone = models.CharField(max_length=15)  # Telefon
    email = models.EmailField()  # Mail
    agreement_amount = models.DecimalField(max_digits=10, decimal_places=2)  # Yeni davanın anlaşma bedeli
    amount_received = models.DecimalField(max_digits=10, decimal_places=2)  # Alınan para
    remaining_balance = models.DecimalField(max_digits=10, decimal_places=2)  # Kalan bakiye
    file_expenses = models.DecimalField(max_digits=10, decimal_places=2)  # Dosya masrafları
    last_sms_date = models.DateField(null=True, blank=True)  # En son SMS atma tarihi
    files = models.TextField()  # Müvekkilin dosyaları

    # Ek sütunlar
    created_at = models.DateTimeField(auto_now_add=True)  # Oluşturulma tarihi
    updated_at = models.DateTimeField(auto_now=True)  # Güncellenme tarihi
    notes = models.TextField(blank=True, null=True)  # Notlar

    def __str__(self):
        return f"{self.tc} - {self.email}"


class Case(models.Model):
    """
    Model to store information about legal cases associated with clients.

    Attributes:
        id (AutoField): Unique identifier for the case, automatically incremented.
        client (ForeignKey): The client associated with this case.
        case_number (str): Unique case number.
        case_type (str): Type of the case (e.g., criminal, civil, labor).
        status (str): Current status of the case (e.g., ongoing, resolved, closed).
        start_date (DateField): Date when the case started.
        end_date (DateField): Date when the case ended (if resolved).
        hearing_date (DateField): Date of the court hearing.
        court (str): The court where the case is being heard.
        description (TextField): A brief description of the case.
        created_at (DateTimeField): Timestamp when the case record was created.
        updated_at (DateTimeField): Timestamp when the case record was last updated.
    """
    
    id = models.AutoField(primary_key=True)  # Otomatik artan ve unique id
    client = models.ForeignKey(Client, on_delete=models.CASCADE)  # Müvekkil ile ilişki
    case_number = models.CharField(max_length=50, unique=True)  # Dava numarası
    case_type = models.CharField(max_length=30)                 # Dava türü
    status = models.CharField(max_length=20)                    # Dava durumu
    start_date = models.DateField()                             # Başlangıç tarihi
    end_date = models.DateField(null=True, blank=True)          # Bitiş tarihi
    hearing_date = models.DateField(null=True, blank=True)      # Duruşma tarihi
    court = models.CharField(max_length=100)                    # Mahkeme
    description = models.TextField(blank=True, null=True)       # Dava açıklaması
    created_at = models.DateTimeField(auto_now_add=True)        # Oluşturulma tarihi
    updated_at = models.DateTimeField(auto_now=True)            # Güncellenme tarihi
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # User tracking
    case_file = models.FileField(upload_to='case_files/', blank=True, null=True)  # File upload

    def __str__(self):
        return f"{self.case_number} - {self.client}"
    

def get_upload_path(instance, filename):
    ext = filename.split('.')[-1].lower()
    folder_name = {
        'pdf': 'uploads/pdf_files',
        'xls': 'uploads/excel_files',
        'xlsx': 'uploads/excel_files',
        # Diğer uzantılar burada tanımlanabilir
    }.get(ext, 'uploads/other_files')

    return os.path.join(folder_name, filename)

class DailyFile(models.Model):
    id = models.AutoField(primary_key=True)  # Otomatik artan ve unique id
    file = models.FileField(upload_to="uploads/daily_files",unique=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name
    
class UploadedFile(models.Model):
    from Client.models import Case
    id = models.AutoField(primary_key=True)  # Otomatik artan ve unique id
    
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    file = models.FileField(upload_to=get_upload_path, unique=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name
    

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
