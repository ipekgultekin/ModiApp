# run_create_db.py
from backend.app.database import Base, engine
import backend.app.models  # modellerin yüklenmesi önemli!

Base.metadata.create_all(bind=engine)
print("✅ Veritabanı oluşturuldu.")
