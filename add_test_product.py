from backend.app.database import SessionLocal
from backend.app import models

db = SessionLocal()

product = models.TrackedProduct(
    title="Test Elbise",
    url="https://www.zara.com/tr/tr/kisa-elbise-p04813302.html?v1=415178110&v2=2220625&origin=shopcart",
    site_name="Zara",
    user_id=1  # Bu kullanıcı ID'si mevcut olmalı
)

db.add(product)
db.commit()
print("✅ Test ürünü eklendi.")
db.close()
