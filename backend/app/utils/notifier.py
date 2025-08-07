import requests
from bs4 import BeautifulSoup
from backend.app import models
from sqlalchemy.orm import Session
from plyer import notification
from backend.app.utils.email_sender import send_stock_email  # 📧 E-posta fonksiyonunu ekledik

def check_stock_status(url: str) -> bool:
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        # Basit kontrol (siteye özel değişebilir!)
        if "out of stock" in soup.text.lower() or "tükendi" in soup.text.lower():
            return False
        return True
    except Exception as e:
        print(f"🔴 Hata oluştu: {url} kontrol edilemedi → {e}")
        return False

def notify_user(title: str, message: str):
    try:
        notification.notify(
            title=title,
            message=message,
            timeout=6
        )
    except Exception as e:
        print(f"❌ Masaüstü bildirimi gönderilemedi: {e}")

def run_stock_check(db: Session):
    products = db.query(models.TrackedProduct).all()
    for product in products:
        in_stock = check_stock_status(product.url)
        if in_stock:
            user = product.owner

            # Masaüstü bildirimi
            notify_user("Modi App", f"{product.title or 'Bir ürün'} stokta! ({product.site_name})")

            # E-posta bildirimi
            send_stock_email(
                to=user.email,
                product_name=product.title or 'Bir ürün',
                product_url=product.url,
                brand=product.site_name or "Bilinmiyor"
            )

            print(f"🟢 {product.url} artık stokta ve kullanıcıya bildirildi.")
        else:
            print(f"🔴 {product.url} hala stokta değil.")
