import google.generativeai as genai
import os
from dotenv import load_dotenv
import logging
from google.api_core import exceptions as api_exceptions
import requests


# Logging ayarları
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# .env dosyasını yükle
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    logging.error("GOOGLE_API_KEY bulunamadı. Lütfen .env dosyanızı kontrol edin.")
    raise ValueError("API anahtarı eksik. Uygulama başlatılamaz.")

# Model adı (AI Studio ile uyumlu)
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

# Chat handler
def handle_chat(message: str, style: str = "casual", favorite_brands: str = "Zara, Bershka") -> str:
    try:
        model = genai.GenerativeModel(TARGET_MODEL)
        chat = model.start_chat(history=[])

        full_prompt = (
            f"Sen bir kişisel moda asistanısın. Kullanıcının mesajında belirttiği **sadece o kıyafet türü için** "
            f"ürün öner. Yalnızca ürün adı ve marka ver. Açıklama, fiyat veya link verme.\n\n"
            f"Stil: {style}\n"
            f"Favori markalar: {favorite_brands}\n"
            f"Kullanıcı mesajı: {message}\n\n"
            f"Yanıt formatı:\n"
            f"Kırmızı Ceket - Marka: Zara\n"
            f"Mavi Pantolon - Marka: Bershka"
        )

        logging.info(f"Oluşturulan prompt: {full_prompt}")
        response = chat.send_message(full_prompt)
        raw_lines = response.text.strip().split("\n")

        enriched_response = []
        for line in raw_lines:
            if not line.strip():
                continue
            try:
                product_part, brand_part = line.split(" - Marka:")
                product = product_part.strip()
                brand = brand_part.strip()
                link = generate_brand_search_link(product, brand)

                # HTML anchor tag ile döndür
                link_html = f"<a href='{link}' target='_blank' class='text-blue-600 underline'>{link}</a>"
                enriched_response.append(f"🛍️ {product} - Marka: {brand} <br>🔗 {link_html}")
            except Exception as e:
                enriched_response.append(f"{line} <br>❌ Arama hatası: {e}")

        return "<br><br>".join(enriched_response)

    except genai.types.BlockedPromptException as e:
        logging.error(f"Prompt engellendi - {e}")
        return "❗ AI isteğiniz güvenlik nedeniyle engellendi. Lütfen farklı bir şey deneyin."
    except api_exceptions.NotFound as e:
        logging.error(f"Model bulunamadı - {e}")
        return "❗ Moda danışmanı modeli şu anda kullanılamıyor. Daha sonra tekrar deneyin."
    except api_exceptions.GoogleAPICallError as e:
        logging.error(f"API çağrı hatası - {e}")
        return "❗ AI servisleriyle iletişim kurulamadı. Lütfen tekrar deneyin."
    except Exception as e:
        logging.error(f"Genel hata: {e}", exc_info=True)
        return f"❗ Bir hata oluştu: {str(e)}"


def search_product_on_google(product, brand):
    brand = brand.lower()
    product_encoded = product.replace(" ", "+")  # URL uyumlu hale getir

    brand_search_urls = {
        "zara": f"https://www.zara.com/tr/tr/search?searchTerm={product_encoded}",
        "bershka": f"https://www.bershka.com/tr/search?q={product_encoded}",
        "mango": f"https://shop.mango.com/tr/kadin/arama?q={product_encoded}",
        "stradivarius": f"https://www.stradivarius.com/tr/search?q={product_encoded}",
        "pull and bear": f"https://www.pullandbear.com/tr/search?q={product_encoded}"
    }

    for key in brand_search_urls:
        if key in brand:
            return brand_search_urls[key]

    # Eğer eşleşme yoksa Google araması öner:
    return f"https://www.google.com/search?q={product_encoded}+{brand}"


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

    # Eşleşme bulunmazsa genel Google araması döndür
    return f"https://www.google.com/search?q={product_encoded}+{brand}"
