import mysql.connector
from mysql.connector import Error

def list_tables(host, user, password, database):
    try:
        # Veritabanı bağlantısını oluştur
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

        if connection.is_connected():
            print("Bağlantı başarılı!")
            cursor = connection.cursor()
            # Tabloları listele
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            
            print("Veritabanındaki tablolar:")
            for table in tables:
                print(table[0])
    
    except Error as e:
        print(f"Bağlantı hatası: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Bağlantı kapatıldı.")

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'DavaTakipSistemi',  # Uzaktaki veritabanı adı
        'USER': 'root',    # MySQL kullanıcı adı
        'PASSWORD': '1453.',         # MySQL şifresi
        'HOST': '77.92.154.83',    # Uzak MySQL sunucusunun IP adresi veya alan adı
        'PORT': '3306',              # MySQL varsayılan portu (genelde 3306)
    }
}
# Kullanıcı bilgilerini tanımlayın
host = '77.92.154.83'  # Uzaktaki veritabanı sunucusunun IP adresi
user = 'root'   # Veritabanı kullanıcı adı
password = '1453.'       # Veritabanı parolası
database = 'DavaTakipSistemi'  # Veritabanı adı

# Fonksiyonu çağırın
list_tables(host, user, password, database)
