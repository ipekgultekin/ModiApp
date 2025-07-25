# 👗 ModiApp – AI Destekli Moda Asistanı

ModiApp, kullanıcıların kişisel stil tercihlerine ve favori markalarına göre kıyafet önerileri sunan yapay zeka destekli bir web uygulamasıdır.  
Google Gemini AI ile entegre çalışır ve interaktif bir sohbet arayüzü sağlar.

---

## 🚀 Özellikler

- 🧠 Google Gemini AI ile doğal dil işleme
- 👚 Kullanıcının stiline özel kıyafet önerileri
- 💬 Gerçek zamanlı AI destekli sohbet arayüzü
- 🔐 JWT ile kullanıcı kimlik doğrulama
- 🌐 FastAPI + Jinja2 + TailwindCSS altyapısı

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

Proje dizinine `.env` adında bir dosya oluşturun ve içine şunları ekleyin:

```
GOOGLE_API_KEY=your_gemini_api_key
SECRET_KEY=mysecretkey123
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

📌 Gemini API anahtarını [https://makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey) adresinden alabilirsiniz.

---

## ▶️ Uygulamayı Başlat

```bash
uvicorn app.main:app --reload
```

Tarayıcıda şu adrese gidin:

```
http://127.0.0.1:8000/mainpage
```
