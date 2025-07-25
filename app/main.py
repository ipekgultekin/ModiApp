from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.routers import auth, users, tracker, pages, chatbot  # ✅ Chatbot eklendi

app = FastAPI()

# CORS ayarları
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Router'ları ekle
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(tracker.router, prefix="/tracker", tags=["Stock Tracker"])
app.include_router(pages.router)  # 👉 HTML sayfaları burada
app.include_router(chatbot.router, prefix="/chat", tags=["Chatbot"])  # ✅ Chat endpoint

# Statik dosyaları bağla
app.mount("/static", StaticFiles(directory="static"), name="static")
