import time
from sqlalchemy.orm import Session
from backend.app.database import SessionLocal
from backend.app.utils.notifier import run_stock_check

def start_checker():
    while True:
        try:
            db: Session = SessionLocal()
            run_stock_check(db)
            db.close()
        except Exception as e:
            print("Otomatik stok kontrol hatası:", e)
        time.sleep(300)  # 5 dakika
