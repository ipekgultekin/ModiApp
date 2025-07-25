# app/schemas.py
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str | None = None

class UserOut(BaseModel):
    id: int
    email: EmailStr
    name: str | None
    created_at: datetime

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str
class ProductCreate(BaseModel):
    url: str
    title: str | None = None
    site_name: str | None = None

class ProductOut(ProductCreate):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True