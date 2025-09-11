import sqlite3
import os
# Eğer tekrar çalıştırınca duplicate istemezsek önce dosyayı sil (isteğe bağlı)
# if os.path.exists("site.db"):
#     os.remove("site.db")

conn = sqlite3.connect("site.db")
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    isim TEXT,
    kategori TEXT,
    dil TEXT,
    foto TEXT,
    aciklama TEXT
)
""")

# Örnek veriler (foto dosyalarının static klasöründe olduğundan emin ol)
examples = [
    ("Ali Yılmaz", "yazılımcı", "Python", "/static/ali.jpg", "3 yıllık Python geliştiricisi, Django & Flask deneyimi"),
    ("Ayşe Demir", "yazılımcı", "Java", "/static/ayse.jpg", "Kurumsal Java uygulamaları ve Spring boot tecrübesi"),
    ("Mehmet Can", "yazılımcı", "C#", "/static/mehmet.jpg", "Unity ve .NET ile oyun & uygulama geliştirme"),
    ("Zeynep Kaya", "yazılımcı", "C++", "/static/zeynep.jpg", "Performans optimizasyonu ve oyun motoru geliştirme"),
    ("Bora Ak", "yazılımcı", "Javascript", "/static/bora.jpg", "Front-end deneyimi (JS olmasa bile örnek kayıt)"),
    ("Elif Solmaz", "yazılımcı", "Ruby", "/static/elif.jpg", "Rails ile CRUD uygulamaları")
]

# Ekle (aynı veriyi tekrar eklememek için basit kontrol isteğe bağlı)
for item in examples:
    c.execute("INSERT INTO users (isim, kategori, dil, foto, aciklama) VALUES (?, ?, ?, ?, ?)", item)

conn.commit()
conn.close()
print("DB hazırlandı ve örnek veriler eklendi.")
