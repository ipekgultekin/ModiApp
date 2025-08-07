# app/routers/tracker.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app import models, schemas
from backend.app.database import SessionLocal
from backend.app.routers.auth import get_current_user
from typing import List

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/add", response_model=schemas.ProductOut)
def add_product(product: schemas.ProductCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    new_item = models.TrackedProduct(**product.dict(), owner=current_user)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item

@router.get("/my-products", response_model=List[schemas.ProductOut])
def get_my_products(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return db.query(models.TrackedProduct).filter(models.TrackedProduct.user_id == current_user.id).all()

@router.delete("/delete/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    product = db.query(models.TrackedProduct).filter_by(id=product_id, user_id=current_user.id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    return {"detail": "Product deleted"}
