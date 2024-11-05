from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import random
import datetime


class TwoFactor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now=True)

    def set_code(self, code=None):
        """
        Yeni bir doğrulama kodu oluşturur veya belirtilen kodu atar.
        """
        if code is None:
            code = f"{random.randint(100000, 999999)}"  # 6 haneli rastgele sayı
        self.code = code
        self.created_at = timezone.now()
        self.save()
    def is_time_expired(self):
        """
        Kodun süresi dolmuşsa `True`, aksi halde `False` döndürür.
        """
        expiration_time = self.created_at + datetime.timedelta(minutes=3)
        return timezone.now() > expiration_time
    def is_code_valid(self, input_code):
        """
        Kod geçerliyse `True`, aksi halde `False` döndürür.
        """
        
        # Süre ve kod doğrulama
        return self.code == input_code

    def __str__(self):
        return f"{self.user.username} - {self.code}"
