from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from backend.app.database import SessionLocal
from backend.app.models import StylePreference, User

templates = Jinja2Templates(directory="frontend/templates")
router = APIRouter()

# 🔌 DB bağlantısı
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 🏠 Dashboard Sayfası (Kök URL)
@router.get("/", response_class=HTMLResponse)
async def dashboard_page(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})


# 🔐 Login Sayfası
@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


# 🧍‍♀️ Register Sayfası
@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


# 🎯 Stil Testi - GET
@router.get("/style-test", response_class=HTMLResponse)
async def style_test_page(request: Request, db: Session = Depends(get_db)):
    user_id = request.cookies.get("user_id")
    if not user_id:
        return RedirectResponse(url="/login", status_code=302)

    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        return RedirectResponse(url="/login", status_code=302)

    if user.has_taken_style_test:
        return RedirectResponse(url="/mainpage", status_code=302)

    return templates.TemplateResponse("style_test.html", {"request": request, "user": user})


# 🎯 Stil Testi - POST
@router.post("/style-test")
async def submit_style_test(
    request: Request,
    style: str = Form(...),
    brands: str = Form(""),
    avoid_colors: str = Form(""),
    db: Session = Depends(get_db)
):
    user_id = request.cookies.get("user_id")
    if not user_id:
        return RedirectResponse(url="/login", status_code=302)

    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        return RedirectResponse(url="/login", status_code=302)

    pref = StylePreference(
        user_id=user.id,
        style=style,
        favorite_brands=brands,
        avoid_colors=avoid_colors
    )
    db.add(pref)
    user.has_taken_style_test = True
    db.commit()

    return RedirectResponse(url="/mainpage", status_code=302)


# 🏠 Mainpage (Test sonrası ekran)
@router.get("/mainpage", response_class=HTMLResponse)
async def main_page(request: Request, db: Session = Depends(get_db)):
    user_id = request.cookies.get("user_id")
    if not user_id:
        return RedirectResponse(url="/login", status_code=302)

    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        return RedirectResponse(url="/login", status_code=302)

    user_style_pref = db.query(StylePreference).filter(StylePreference.user_id == user.id).first()

    user_style = user_style_pref.style if user_style_pref and user_style_pref.style else "casual"
    recommended_products = get_style_recommendations(user_style)

    return templates.TemplateResponse("mainpage.html", {
        "request": request,
        "user": user,
        "recommended_products": recommended_products,
        "user_style": user_style
    })


# 🔐 Çıkış (Logout)
@router.post("/logout")
async def logout():
    response = RedirectResponse(url="/", status_code=302)
    response.delete_cookie("user_id")
    return response


# 🧠 Fake öneri sistemi
def get_style_recommendations(user_style):
    return [
        {
            "name": f"{user_style.title()} Hoodie",
            "image": "https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=300&h=400&fit=crop",
            "price": "₺349",
            "brand": "Zara",
            "description": f"{user_style.title()} stiline uygun günlük hoodie"
        },
        {
            "name": f"{user_style.title()} Pantolon",
            "image": "https://images.unsplash.com/photo-1542272604-787c3835535d?w=300&h=400&fit=crop",
            "price": "₺279",
            "brand": "Mavi",
            "description": f"Konforlu ve şık {user_style} pantolonu"
        }
    ]
