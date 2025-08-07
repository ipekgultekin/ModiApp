# 🤖 Automation: Fallback Agent

Bu ajan, kullanıcının kıyafetle ilgili yaptığı aramaları otomatik olarak vektör tabanlı sistem (FAISS) veya web arama yönlendirmesi arasında yönlendirir.

## 🎯 Amaç
Kullanıcı bir ürün istediğinde sistem:
- Öncelikle FAISS vektör veritabanında eşleşen ürünleri arar.
- Eğer yeterli eşleşme bulunamazsa, ilgili markanın (örneğin Zara, Bershka) arama sayfasına yönlendiren bir bağlantı oluşturur.

## ⚙️ Çalışma Mantığı
1. Kullanıcının mesajı `fallback_agent.py` fonksiyonuna gönderilir.
2. FAISS ile vektör arama yapılır.
3. Eğer eşleşen ürün varsa → `type: "vector_result"` döner.
4. Eğer eşleşme yoksa → `type: "fallback_link"` ve bir arama linki döner.
5. `ai_chat.py` bu sonucu kontrol eder ve ya AI ile öneri üretir ya da doğrudan bağlantı gösterir.

## 📁 Kullanılan Dosyalar
- `features/search_products.py`
- `features/web_search_tool.py`
- `agents/fallback_agent.py`
- `features/ai_chat.py` (entegre kullanım)

## 🧪 Test Etmek İçin
Aşağıdaki gibi zorlayıcı cümleler yaz:
- "Zara'dan mavi kürklü kapüşonlu mont istiyorum"
- "Çiçekli mor gece elbisesi arıyorum"
- "Oversize desenli yelek Bershka"

Eğer bu ürünler FAISS'te yoksa, sistem seni otomatik olarak Zara, Bershka veya Google'a yönlendirir.

