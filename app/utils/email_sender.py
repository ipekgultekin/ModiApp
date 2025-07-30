# app/utils/email_sender.py
import smtplib
import os
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")


def send_stock_email(to_email: str, product_title: str, product_url: str):
    subject = f"{product_title} ürünü stokta!"
    body = f"{product_title} yeniden stokta görünüyor!\nİncele: {product_url}"

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_USER
    msg["To"] = to_email

    try:
        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASS)
            server.sendmail(EMAIL_USER, to_email, msg.as_string())
        print("✅ E-posta başarıyla gönderildi.")
    except Exception as e:
        print(f"❌ E-posta gönderme hatası: {e}")
