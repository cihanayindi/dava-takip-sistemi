import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

def eposta_gonder(konu, mesaj, kime):
    msg = EmailMessage()
    msg.set_content(mesaj)
    msg['Subject'] = konu
    msg['To'] = kime

    # Kullanıcı bilgilerini .env dosyasından al
    user = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASSWORD")
    msg['From'] = user

    # E-posta gönderme işlemi
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(user, password)
    server.send_message(msg)
    server.quit()
    print("Mesaj gönderildi")

# if __name__ == '__main__':
#     eposta_gonder("alarm", "merhaba Mr. Çilek, alanda insan algılandı", "epostayedek799@gmail.com")

