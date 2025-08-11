
import google.generativeai as genai
import os
from dotenv import load_dotenv
import logging
from google.api_core import exceptions as api_exceptions
from backend.features.web_search_tool import get_fallback_search_link
from backend.agents.fallback_agent import fallback_agent
import re
import json
from pathlib import Path

# Logging ayarları
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# .env dosyasını yükle
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    logging.error("GOOGLE_API_KEY bulunamadı. Lütfen .env dosyanızı kontrol edin.")
    raise ValueError("API anahtarı eksik. Uygulama başlatılamaz.")

TARGET_MODEL = "models/gemini-1.5-flash-latest"

try:
    genai.configure(api_key=API_KEY)
    logging.info("Google Generative AI yapılandırıldı.")

    logging.info("Uygun modeller listeleniyor...")
    available_models = [m.name for m in genai.list_models() if "generateContent" in m.supported_generation_methods]

    if TARGET_MODEL not in available_models:
        logging.error(f"Model '{TARGET_MODEL}' desteklenmiyor. Mevcut modeller: {available_models}")
        raise Exception(f"AI modeli bulunamadı: {TARGET_MODEL}")

    logging.info(f"Kullanılacak model: {TARGET_MODEL}")

except Exception as e:
    logging.error(f"Model yapılandırma hatası: {e}")
    raise Exception(f"AI servisleri başlatılamıyor: {e}")

def get_relevant_products(user_message, limit=5):
    # backend/ dizinine git → data/products.json'u aç
    data_path = Path(__file__).resolve().parents[1] / "data" / "products.json"
    print(f"[DEBUG] products.json path: {data_path}")

    if not data_path.exists() or data_path.stat().st_size == 0:
        # Dosya yoksa veya boşsa güvenli dönüş
        return []

    with data_path.open("r", encoding="utf-8-sig") as f:
        products = json.load(f)

    keywords = user_message.lower().split()
    scored = []
    for p in products:
        text = (p.get("description","") + " " + p.get("title","")).lower()
        score = sum(1 for kw in keywords if kw in text)
        if score > 0:
            scored.append((score, p))

    scored.sort(reverse=True, key=lambda x: x[0])
    return [item[1] for item in scored[:limit]]

def handle_chat(message: str, style: str = "casual", favorite_brands: str = "Zara, Bershka") -> str:
    try:
        relevant_products = get_relevant_products(message)
        if not relevant_products:
            fallback_url = get_fallback_search_link(message)
            return (
                f"❗ Üzgünüm, veritabanımda bu ürünü bulamadım. "
                f"Aşağıdaki bağlantıdan arayabilirsin:<br><br>"
                f"<a href='{fallback_url}' target='_blank' class='text-blue-600 underline'>{fallback_url}</a>"
            )

        product_text = "\n".join([
            f"- {p['title']} ({p['brand']}) – {p['price']} TL: {p['description']}"
            for p in relevant_products
        ])

        model = genai.GenerativeModel(TARGET_MODEL)
        chat = model.start_chat(history=[])

        full_prompt = (
            f"Sen bir kişisel moda asistanısın. Kullanıcının aradığı kiyafetleri aşağıda göreceğin ürün listesi içinden önermek zorundasın. "
            f"Liste dışına çıkamazsın. Uygun ürün olmasa bile en benzer 2-3 tanesini seç.\n\n"
            f"📌 Ürün listesi:\n{product_text}\n\n"
            f"👤 Kullanıcı mesajı: {message}\n"
            f"👗 Stil: {style}, Favori Markalar: {favorite_brands}\n\n"
            f"🔁 Lütfen aşağıdaki ürünleri önerirken sadece ürün adı ve markayı belirt. "
            f"Açıklama, yorum, madde işareti, yıldız, kalın yazı veya emoji ekleme.\n"
            f"⛔ Yalnızca ürün adı ve markayı yaz. Şunları ASLA yazma: açıklama, maalesef, öneriyorum, cümle, <br>, ⭐, 🎯, emoji, yorum.\n"
            f"✅ Sadece bu şekilde cevap ver: Ürün Adı Marka\n"
            f"Örnek: Red Denim Jacket Zara"
        )

        logging.info(f"Oluşturulan prompt: {full_prompt}")
        response = chat.send_message(full_prompt)
        raw_lines = response.text.strip().split("\n")

        enriched_response = []
        for line in raw_lines:
            if not line.strip():
                continue
            try:
                match = re.search(r"^(.*?)\s+([A-Z][a-z]+)$", line.strip())
                if not match:
                    enriched_response.append(f"{line} <br>❌ Format tanınamadı.")
                    continue

                product = match.group(1).strip()
                brand = match.group(2).strip()

                link = generate_brand_search_link(product, brand)
                link_html = f"<a href='{link}' target='_blank' class='text-blue-600 underline'>{link}</a>"
                enriched_response.append(f"🏍️ {product} - Marka: {brand} <br>🔗 {link_html}")
            except Exception as e:
                enriched_response.append(f"{line} <br>❌ Arama hatası: {e}")

        return "<br><br>".join(enriched_response)

    except Exception as e:
        logging.error(f"Hata: {e}", exc_info=True)
        return "❗ Bir hata oluştu. Lütfen daha sonra tekrar deneyin."

def generate_brand_search_link(product, brand):
    product_encoded = product.replace(" ", "+").lower()
    brand = brand.lower()

    brand_links = {
        "zara": f"https://www.zara.com/tr/tr/search?searchTerm={product_encoded}",
        "bershka": f"https://www.bershka.com/tr/search?q={product_encoded}",
        "mango": f"https://shop.mango.com/tr/kadin/arama?q={product_encoded}",
        "stradivarius": f"https://www.stradivarius.com/tr/search?q={product_encoded}",
        "pull and bear": f"https://www.pullandbear.com/tr/search?q={product_encoded}"
    }

    for key in brand_links:
        if key in brand:
            return brand_links[key]

    return f"https://www.google.com/search?q={product_encoded}+{brand}"
