import mysql.connector
from mysql.connector import Error

def execute_query(host, user, password, database):
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
            cursor = connection.cursor(buffered=True)  # Buffered olarak cursor oluştur
            
            while True:
                # Kullanıcıdan sorgu al
                query = input("SQL sorgusunu girin (Çıkmak için 'exit' yazın): ")
                
                # Çıkış koşulu
                if query.lower() == 'exit':
                    print("Programdan çıkılıyor.")
                    break
                
                try:
                    # Sorguyu çalıştır ve sonucu yazdır
                    cursor.execute(query)
                    
                    # Sorgunun türüne göre sonuçları işle
                    if query.strip().lower().startswith("select") or query.strip().lower().startswith("show"):
                        results = cursor.fetchall()
                        for row in results:
                            print(row)
                    else:
                        # Diğer sorgular için (INSERT, UPDATE, DELETE vb.) etkilenen satır sayısını yazdır
                        connection.commit()
                        print(f"{cursor.rowcount} satır etkilendi.")
                
                except Error as e:
                    print(f"Sorgu hatası: {e}")
    
    except Error as e:
        print(f"Bağlantı hatası: {e}")
    
    finally:
        # Bağlantıyı kapat
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Bağlantı kapatıldı.")

# Veritabanı bilgilerini tanımlayın
host = '77.92.154.83'  # Uzaktaki veritabanı sunucusunun IP adresi
user = 'root'          # Veritabanı kullanıcı adı
password = '1453.'     # Veritabanı parolası
database = 'DavaTakipSistemi'  # Veritabanı adı

# Fonksiyonu çağırın
execute_query(host, user, password, database)
