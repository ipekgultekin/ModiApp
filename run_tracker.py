# run_tracker.py
from app.database import SessionLocal
from app.utils.notifier import run_stock_check

if __name__ == "__main__":
    print("🔍 Ürün stokları kontrol ediliyor...")
    db = SessionLocal()
    run_stock_check(db)
    db.close()
