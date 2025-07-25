import google.generativeai as genai
import os
from dotenv import load_dotenv
import logging
from google.api_core import exceptions as api_exceptions

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    logging.error("GOOGLE_API_KEY bulunamadı. Lütfen .env dosyanızı kontrol edin.")
    raise ValueError("API anahtarı eksik. Uygulama başlatılamaz.")

# KULLANILACAK HEDEF MODELİ BURADA DÜZELTİYORUZ
# Listeden kontrol ettiğimiz tam model adını kullanıyoruz: 'models/gemini-1.5-flash-latest'
TARGET_MODEL = "models/gemini-1.5-flash-latest" 
# Alternatif olarak, eğer bu çalışmazsa 'models/gemini-1.5-pro-latest' veya 'models/gemini-1.5-pro' deneyebilirsiniz.

try:
    genai.configure(api_key=API_KEY)
    logging.info("Google Generative AI yapılandırıldı.")
    
    logging.info("Erişilebilir Gemini modelleri kontrol ediliyor...")
    available_models = []
    for m in genai.list_models():
        if "generateContent" in m.supported_generation_methods:
            available_models.append(m.name)
    logging.info(f"generateContent destekleyen modeller: {available_models}")

    if TARGET_MODEL not in available_models:
        logging.error(f"Hata: Belirlenen hedef model '{TARGET_MODEL}' erişilebilir modeller arasında bulunamadı. Lütfen ListModels çıktısını kontrol edin.")
        # Bu durumda uygulama başlatılmamalı, çünkü doğru model bulunamadı.
        raise Exception(f"AI servisleri başlatılamıyor: Hedef model '{TARGET_MODEL}' erişilebilir değil. Mevcut modeller: {available_models}")
    
    logging.info(f"Kullanılacak AI modeli: {TARGET_MODEL}")


except Exception as e:
    logging.error(f"Google Generative AI yapılandırma veya model listeleme hatası: {e}")
    # Bu hata mesajı, uygulamanın başlatılmasını engelleyen nihai hatayı gösterir.
    raise Exception(f"AI servisleri başlatılamıyor: {e}")


def handle_chat(message: str, style: str = "casual", favorite_brands: str = "Zara, Bershka") -> str:
    """
    Kullanıcının mesajına göre kıyafet önerisi oluşturan ana sohbet işleyicisi.
    """
    try:
        model = genai.GenerativeModel(TARGET_MODEL) 
        chat = model.start_chat(history=[]) 

        full_prompt = (
            f"Sen bir kişisel moda asistanısın. Kullanıcının mesajında belirttiği **sadece o spesifik kıyafet türü için** "
            f"kıyafet önerisi yapmalısın. Eğer kullanıcı birden fazla kıyafet türü isterse, her biri için ayrı ayrı öneri yap. "
            f"Açıklama ve görsel linkleri (gerçek olmayan) ile birlikte ver, yorum yapma ve yalnızca öneriyi sun.\n\n"
            f"Stil tercihi: {style}\n"
            f"Favori markalar: {favorite_brands}\n"
            f"Kullanıcının mesajı: {message}\n\n"
            f"Örnek format:\n"
            f"Kırmızı tişört - Marka: Zara - Link: [https://example.com/kirmizi-tisort](https://example.com/kirmizi-tisort)\n"
            f"Mavi pantolon - Marka: Bershka - Link: [https://example.com/mavi-pantolon](https://example.com/mavi-pantolon)\n"
            f"Yeşil ceket - Marka: Mango - Link: [https://example.com/yesil-ceket](https://example.com/yesil-ceket)"
        )
        logging.info(f"Oluşturulan prompt: {full_prompt}")

        response = chat.send_message(full_prompt)
        logging.info(f"AI'dan gelen yanıt: {response.text}")
        
        return response.text

    except genai.types.BlockedPromptException as e:
        logging.error(f"AI işlem hatası: Prompt engellendi - {e}")
        return "Üzgünüz, isteğiniz güvenlik politikalarımız tarafından engellendi. Lütfen farklı bir ifade deneyin."
    except api_exceptions.NotFound as e: 
        logging.error(f"AI işlem hatası: Model bulunamadı veya erişilemez (404 Not Found) - {e}")
        return "AI işlem hatası: Moda danışmanı şu anda hizmet veremiyor. Model bulunamadı veya erişilebilir değil. Lütfen daha sonra tekrar deneyin."
    except api_exceptions.GoogleAPICallError as e: 
        logging.error(f"AI işlem hatası: Google API çağrısı sırasında hata oluştu - {e}")
        return f"AI işlem hatası: AI servisleriyle iletişimde bir sorun oluştu. Detay: {e}"
    except Exception as e:
        logging.error(f"Beklenmedik AI işlem hatası: {e}", exc_info=True)
        return f"Beklenmedik bir AI hatası oluştu: {str(e)}"