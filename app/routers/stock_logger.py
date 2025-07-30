from fastapi import APIRouter, Request
from pydantic import BaseModel
import sqlite3
from datetime import datetime

router = APIRouter()

# Giriş modeli
class StockLog(BaseModel):
    brand: str
    url: str
    size: str

@router.post("/log-stock")
async def log_stock(data: StockLog):
    try:
        conn = sqlite3.connect("trackings.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO stock_logs (brand, url, size, timestamp)
            VALUES (?, ?, ?, ?)
        """, (data.brand, data.url, data.size, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()
        conn.close()
        return {"message": "Stok bilgisi kaydedildi."}
    except Exception as e:
        return {"error": str(e)}
