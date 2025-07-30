import sqlite3

# Veri tabanı dosyasını oluştur
conn = sqlite3.connect("trackings.db")
cursor = conn.cursor()

# Tabloyu oluştur
cursor.execute("""
CREATE TABLE IF NOT EXISTS stock_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    brand TEXT,
    product_url TEXT,
    size TEXT,
    in_stock_time DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
conn.close()

print("✅ trackings.db başarıyla oluşturuldu ve stock_logs tablosu eklendi.")
