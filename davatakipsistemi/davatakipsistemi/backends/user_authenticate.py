import hashlib
from Client.models import CustomUsers

def custom_authenticate(username, password):
    """
    Bu fonksiyona parametre olarak kullanıcı adı ve şifre gelir.
    Fonksiyon, CustomUsers tablosundan kullanıcı adına göre salt değerini alır.
    Kullanıcının girdiği şifreyi salt ile birleştirip sha256 ile hash'ler,
    eğer bu hash tablodaki hashlenmiş şifre ile eşleşiyorsa giriş izni verir.
    """
    try:
        # Kullanıcıyı veritabanında arıyoruz
        user = CustomUsers.objects.get(username=username)
        
        # Kullanıcının salt değerini alıyoruz
        salt = user.salt
        
        # Kullanıcının girdiği şifreyi salt ile birleştirip hashliyoruz
        hashed_password = hashlib.sha256((password + salt).encode()).hexdigest()
        
        # Hesaplanan hash, veritabanındaki hash ile eşleşiyorsa True döndür
        if hashed_password == user.password:
            return True
        else:
            return False
    except CustomUsers.DoesNotExist:
        # Eğer kullanıcı adı bulunamazsa False döndür
        return False

