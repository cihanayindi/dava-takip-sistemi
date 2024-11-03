import pandas as pd

# TXT dosyasının yolunu belirtin
excel_file_path = 'dosya_kayitlari.xlsx'


# TXT dosyasının yolunu belirtin
txt_file_path = 'dosya2.txt'

# Verileri depolamak için bir liste
data = []

# TXT dosyasını satır satır okuyun
with open(txt_file_path, 'r', encoding='utf-8') as file:
    for line in file:
        # Satırı numara ve açıklama olarak böl
        parts = line.strip().split('. ', 1)
        if len(parts) == 2:
            numara, aciklama = parts
            data.append((int(numara), aciklama))
            

# DataFrame'e dönüştür
df = pd.DataFrame(data, columns=["Sayı", "Açıklama"])

# Excel dosyasına yaz
df.to_excel(excel_file_path, index=False)

print(f"{excel_file_path} dosyası başarıyla oluşturuldu.")
