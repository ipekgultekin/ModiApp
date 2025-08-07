# 📦 RAG (Retrieval-Augmented Generation) Sistemi

ModiApp, moda ürünlerine dair daha doğru ve bağlama uygun öneriler yapabilmek için bir **RAG (Retrieval-Augmented Generation)** mimarisi kullanır. Bu yapı, kullanıcı mesajlarına uygun ürünleri vektör uzayında bulur ve AI modeline anlamlı bağlam sağlar.

---

## 🎯 Amaç
Kullanıcının yazdığı ürün isteklerine, sistemde yer alan ürünlerden en yakınlarını bulmak ve bu ürünleri AI'a vererek öneri almayı sağlamaktır.

---

## 🧱 Yapı Taşları

### 1. `products.json`
- Ürün verileri bu dosyada tutulur.
- İçerik örneği:
```json
{
  "title": "Red Denim Jacket",
  "description": "An oversized red denim jacket from Zara...",
  "brand": "Zara",
  "price": "899 TL"
}
```

### 2. `embeddings/embed_products.py`
- Ürün açıklamalarını vektörleştiren script.
- Kullanılan model: `all-MiniLM-L6-v2`
- Oluşturulan dosyalar:
  - `data/product_index.faiss`: FAISS vektör veritabanı
  - `data/product_id_map.json`: ID -> ürün eşleşmeleri

### 3. `features/search_products.py`
- Kullanıcının mesajını vektörleştirir.
- FAISS ile en benzer `top_k` ürünü getirir.
- `search_similar_products(query)` fonksiyonu ile kullanılır.

### 4. `ai_chat.py` Entegrasyonu
- `handle_chat()` fonksiyonu içinde önce `search_similar_products` ile veri getirilir.
- Sonra bu ürünler AI modeline verilir.
- Uygun ürün yoksa `fallback_agent` tetiklenerek Google araması yapılır.

---

## 🔍 Kullanım Akışı

1. Kullanıcı: "Kırmızı Zara mont istiyorum"
2. Sistemin Akışı:
   - `query` -> vektöre dönüştürülür
   - FAISS'ten benzer ürünler alınır
   - AI modeline bu ürünler prompt ile verilir
   - AI, "Red Denim Jacket - Zara" gibi bir öneri döner

---

## 🛠️ Nasıl Geliştirebilirim?
- `products.json` dosyasına daha fazla ürün eklersen öneriler çeşitlenir.
- Gelişmiş embedding modelleri (e.g. `bge-m3`, `text-embedding-3-small`) ile daha iyi eşleşmeler yapılabilir.
- Ürünlere renk, kategori gibi metadata eklersen filtreleme yapılabilir.

---

## ✅ Durum
- [x] Ürün vektörleme ✅
- [x] FAISS veritabanı ✅
- [x] Benzer ürün arama ✅
- [x] AI ile öneri entegrasyonu ✅

---

ModiApp'teki RAG sistemi sayesinde kullanıcılar daha kişiselleştirilmiş, bağlamsal ve isabetli moda önerileri alabilirler. 🎯

