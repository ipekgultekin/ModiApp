# app/utils/notifier.py
import requests
from bs4 import BeautifulSoup
from app import models
from sqlalchemy.orm import Session
from plyer import notification

def check_stock_status(url: str) -> bool:
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        # Zara, Bershka, H&M gibi sitelere özel içerik tag'leri değişebilir.
        if "out of stock" in soup.text.lower() or "tükendi" in soup.text.lower():
            return False
        return True
    except Exception as e:
        print(f"Error checking {url}: {e}")
        return False

def notify_user(title: str, message: str):
    notification.notify(
        title=title,
        message=message,
        timeout=6
    )

def run_stock_check(db: Session):
    products = db.query(models.TrackedProduct).all()
    for product in products:
        in_stock = check_stock_status(product.url)
        if in_stock:
            user = product.owner
            notify_user("Modi App", f"{product.title or 'Bir ürün'} stokta! ({product.site_name})")
            print(f"🟢 {product.url} artık stokta.")
        else:
            print(f"🔴 {product.url} hala stokta değil.")
