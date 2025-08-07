import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()  # .env'den değerleri almak için

EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT"))
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

def send_stock_email(to: str, product_name: str, product_url: str, brand: str):
    subject = f"{brand} - {product_name} Stokta!"
    body = f"""
Merhaba!

'{product_name}' ürünü ({brand}) şu anda stokta görünüyor. Kaçırmadan hemen inceleyin!

🔗 Ürün Linki: {product_url}

Sevgiler,
Modi App Ekibi
"""

    msg = MIMEMultipart()
    msg['From'] = EMAIL_USER
    msg['To'] = to
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)
        server.quit()
        print(f"📧 E-posta gönderildi: {to}")
    except Exception as e:
        print(f"❌ E-posta gönderilemedi: {e}")
