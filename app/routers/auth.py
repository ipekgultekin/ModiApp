# app/routers/auth.py

from fastapi import APIRouter, Depends, Form, HTTPException, status
from sqlalchemy.orm import Session
from starlette.responses import HTMLResponse, RedirectResponse
from app import models, schemas
from app.database import SessionLocal
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
load_dotenv()

# 🔐 JWT Config
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# 🔄 DB session getter
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 🔑 Password
def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# ✅ Authenticator from JWT (used only for /profile endpoint)
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(models.User).filter(models.User.id == int(user_id)).first()
    if user is None:
        raise credentials_exception
    return user


# 🧍‍♀️ REGISTER
@router.post("/register", response_class=HTMLResponse)
def register(
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    existing_user = db.query(models.User).filter_by(email=email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered.")
    
    hashed_pw = pwd_context.hash(password)
    new_user = models.User(email=email, password=hashed_pw, name=name)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # ✅ Set cookie & redirect to style test
    response = RedirectResponse(url="/style-test", status_code=303)
    response.set_cookie(key="user_id", value=str(new_user.id))
    return response


# 🔑 LOGIN
@router.post("/login", response_class=HTMLResponse)
def login(
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    db_user = db.query(models.User).filter_by(email=email).first()
    if not db_user or not verify_password(password, db_user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials.")

    # ✅ Redirect to either dashboard or style test
    redirect_url = "/mainpage" if db_user.has_taken_style_test else "/style-test"
    response = RedirectResponse(url=redirect_url, status_code=302)
    response.set_cookie(key="user_id", value=str(db_user.id))
    return response
    
@router.get("/login", response_class=HTMLResponse)
def login_page():
    from fastapi.responses import FileResponse
    return FileResponse("templates/login.html")


# 👤 Optional JWT-based profile
@router.get("/profile", response_model=schemas.UserOut)
def read_profile(current_user: models.User = Depends(get_current_user)):
    return current_user
