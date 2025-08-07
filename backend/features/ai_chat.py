import google.generativeai as genai
import os
from dotenv import load_dotenv
import logging
from google.api_core import exceptions as api_exceptions
from backend.features.web_search_tool import get_fallback_search_link
from backend.agents.fallback_agent import fallback_agent
import re

# FAISS ürün arama modülü
from backend.features.search_products import search_similar_products

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

def handle_chat(message: str, style: str = "casual", favorite_brands: str = "Zara, Bershka") -> str:
    try:
        response = fallback_agent(message)

        if response["type"] == "vector_result":
            similar_products = response["data"]

            product_text = "\n".join([
                f"- {p['title']} ({p['brand']}) – {p['price']}: {p['description']}"
                for p in similar_products
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
                f"Açıklama, yorum, madde işareti, yıldız, kalın yazı veya emoji ekleme."
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

        elif response["type"] == "fallback_link":
            fallback_url = response["url"]
            return (
                f"❗ Üzgünüm, veritabanımda bu ürünü bulamadım. "
                f"Aşağıdaki bağlantıdan arayabilirsin:<br><br>"
                f"<a href='{fallback_url}' target='_blank' class='text-blue-600 underline'>{fallback_url}</a>"
            )
        else:
            return "❗ Beklenmeyen bir sonuç oluştu."

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
