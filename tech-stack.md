# Tech Stack: Modi App - AI Destekli Moda Keşif & Stok Takip Uygulaması

## 🔧 Backend
- **Dil:** Python
- **Framework:** FastAPI (async destekli, hızlı API geliştirme)
- **Veritabanı:** SQLite (başlangıç için) → PostgreSQL (gelişmiş yapı için)
- **ORM:** SQLAlchemy
- **Bildirim:** Plyer / Web push (desktop notification)

## 🧠 AI Entegrasyonu
- **LLM:** Gemini Pro / OpenAI GPT-3.5 (ürün karşılaştırma, alternatif öneri)
- **Scraping:** Playwright veya Requests + BeautifulSoup (ürün linklerinden veri çekme)
- **Benzerlik Algoritması:** Sentence Transformers + cosine similarity

## 💻 Frontend
- **HTML + Tailwind CSS + Vanilla JS** (kullanıcı dostu arayüz için)
- **Alternatif:** Streamlit (hızlı prototipleme)

## 🔐 Kullanıcı Giriş Sistemi
- JWT tabanlı kullanıcı doğrulama
- Şifrelenmiş kayıt işlemi
- Kullanıcı profili ve takibi

## 🚀 Deployment
- **Versiyon kontrol:** GitHub
- **Canlıya alma:** Vercel / Render / Railway
- **Tanıtım sayfası:** GitHub Pages veya Canva + Notion portfolyo

## 🧰 Diğer Araçlar
- **Requests:** AI API ve scraping için
- **dotenv:** Anahtar ve API yönetimi
- **Uvicorn:** FastAPI için ASGI server
