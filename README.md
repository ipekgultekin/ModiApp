
# 👗 ModiApp – AI Destekli Moda Asistanı

ModiApp, kullanıcıların kişisel stil tercihlerine ve favori markalarına göre kıyafet önerileri sunan, yapay zeka destekli bir web uygulamasıdır.  
Google Gemini AI ile entegre çalışır ve kullanıcılarla gerçek zamanlı sohbet ederek kişiselleştirilmiş alışveriş deneyimi sağlar.

---

## 🚀 Özellikler

- 🧠 **Google Gemini AI** ile doğal dil işleme
- 🎯 **FAISS Vektör Arama** ile ürün açıklamaları üzerinden RAG
- 👚 **Stil Testi & Kişiselleştirme** akışı
- 💬 **Gerçek zamanlı chat arayüzü** ile ürün önerileri
- 🔐 **JWT kimlik doğrulama**
- 🌐 **FastAPI** backend + **Jinja2** frontend + **TailwindCSS** stil

---

## 🔧 Kurulum Adımları

### 1️⃣ Projeyi Klonla

```bash
git clone https://github.com/kullaniciadi/modiapp.git
cd modiapp
```

### 2️⃣ Sanal Ortam Oluştur ve Aktifleştir

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Gereken Paketleri Kur

```bash
pip install -r requirements.txt
```

---

## 🔐 Ortam Değişkenleri (.env)

Proje dizinine `.env` adında bir dosya oluşturun:

```env
# ✅ Gemini API Anahtarı (Sohbet motoru için)
GOOGLE_API_KEY=YOUR_GEMINI_API_KEY

# ✅ Google Search API Anahtarı ve Arama Motoru Kimliği (Fallback arama için)
GOOGLE_SEARCH_API_KEY=YOUR_GOOGLE_SEARCH_API_KEY
GOOGLE_CSE_ID=YOUR_GOOGLE_CSE_ID

# ✅ Mail Gönderimi (Şifre sıfırlama, bildirimler vb.)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=YOUR_EMAIL_ADDRESS
EMAIL_PASS=YOUR_APP_PASSWORD  # Gmail için uygulama şifresi olmalı

# ✅ JWT Ayarları (Kimlik doğrulama için)
SECRET_KEY=mysecretkey1234
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

➡️ [Gemini API anahtarı için tıkla](https://makersuite.google.com/app/apikey)

---

## ▶️ Uygulamayı Başlat

```bash
uvicorn app.main:app --reload
```

Tarayıcıda şu adrese gidin:

```
http://127.0.0.1:8000/mainpage
```

---

## 📌 Capstone Proje Aşamaları

### ✅ Tamamlananlar

- ✅ **Fikir & Kullanıcı Akışı**: Moda sektöründe “stokta bulunamayan ürün” problemini çözmek için AI destekli öneri sistemi tasarlandı.
- ✅ **Gemini AI Entegrasyonu**: Kullanıcının mesajına göre ilgili ürünler öneriliyor.
- ✅ **FAISS & RAG**: products.json üzerinden ürün açıklamaları vektörlenip FAISS veritabanında aranıyor.
- ✅ **Arayüz Entegrasyonu**: Chat mesajları tıklanabilir bağlantılarla destekleniyor.
- ✅ **Prompt Mimarisi**: AI sadece veri kümesinden öneri yapacak şekilde yönlendirildi.
- ✅ **products.json**: Ürün adı, açıklama, renk, fiyat, marka ve görsel içeren yapı oluşturuldu.
- ✅ **Agent Mimarisi (LangChain)**: Web araması yapamayan durumlarda alternatif öneri getirebilen ajan sistemi oluşturuldu.

---

### 🔧 Geliştirme Aşamasında (Yapılacaklar)

- 📹 **Demo Videosu veya GIF**  
  Uygulama kullanımını gösteren kısa bir tanıtım demosu hazırlanacak.

- 🧾 **Notion Portfolyo Sayfası**  
  Projeye dair tüm adımların ve görsellerin yer aldığı bir tanıtım sayfası oluşturulacak.

- 📷 **README’ye Ekran Görüntüsü / GIF**  
  Uygulamanın chat arayüzü, stil testi ve AI cevabı örneği görsellerle desteklenecek.

---

## 🧠 Kullanılan Teknolojiler

| Katman     | Teknoloji                          |
|------------|-------------------------------------|
| Backend    | FastAPI, Python, SQLAlchemy         |
| Frontend   | HTML, TailwindCSS, Jinja2, JS       |
| AI         | Gemini Pro (Google), FAISS (RAG)    |
| Auth       | JWT                                 |
| Veritabanı | SQLite                              |
| Agent      | LangChain                           |
| Deployment | Lokal (uvicorn)                     |

---

