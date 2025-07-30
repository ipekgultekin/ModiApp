✅ ModiApp Otomasyon ve Agent Mimarisine Genel Bakış

1️⃣ Otomasyon: Stok Takibi ve Bildirim Sistemi

Kullanıcılar uygulama üzerinden takip etmek istedikleri ürünün linkini ve bedenini seçerek sistemimize kaydediyor.  
Sistem her 5 dakikada bir arka planda bu ürünlerin stok durumunu kontrol eder:

- Eğer ürün hâlâ stokta değilse ➡️ hiçbir şey yapılmaz.
- Eğer ürün stokta ise:
  - 🔔 **Desktop notification** (plyer ile)
  - 📧 **Email bildirimi** (SMTP ile) gönderilir.

🛠 Kullanılan Teknolojiler
- `BeautifulSoup`: Ürün sayfasından stok bilgisi kazımak için
- `plyer`: Masaüstü bildirimi göndermek için
- `smtplib`: Gmail üzerinden e-posta yollamak için
- `schedule`: 5 dakikada bir otomatik kontrol için

🔁 Arka Plan Süreci (schedule_checker.py)
```python
from app.utils.schedule_checker import start_checker

start_checker()

2️⃣ Agent Mimarisi: Akıllı Moda Asistanı
ModiApp içinde çalışan agents/agent_main.py dosyası bir karar verici agent olarak görev yapar.

🤖 Agent Karar Süreci
Kullanıcının ürün isteği alınır (örn: "Siyah elbise var mı?")

Aşağıdaki sırayla arama yapılır:

🔍 Zara

🔍 Bershka

Eğer iki sitede de ürün bulunamazsa:

💡 Gemini AI modeliyle benzer öneri sunulur

📁 Dosya: agents/agent_main.py
-BeautifulSoup ile site taraması
-Gemini 1.5 Flash API ile fallback öneri üretimi
-Prompt mühendisliği ile stil önerisi

👟 Kullanım
python agents/agent_main.py

📌 Ek Notlar
-.env dosyasında gerekli API anahtarları ve SMTP şifreleri gizli tutulmaktadır
-Otomasyon ve agent yapıları tamamen ayrı servislerde ama aynı uygulama içinde entegre çalışmaktadır