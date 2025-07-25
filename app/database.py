# app/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./modi.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# BU FONKSİYONUN app/database.py İÇİNDE OLDUĞUNDAN EMİN OLUN
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()