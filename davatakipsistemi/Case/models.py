from django.db import models

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
