# run_create_db.py
from app.database import Base, engine
import app.models  # modellerin yüklenmesi önemli!

Base.metadata.create_all(bind=engine)
print("✅ Veritabanı oluşturuldu.")
