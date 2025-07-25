from fastapi import APIRouter, Request
from features.ai_chat import handle_chat
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

router = APIRouter()

@router.post("")
async def chat_endpoint(request: Request):
    """
    Chatbot endpoint'i. Kullanıcıdan gelen mesajı işler ve AI yanıtını döndürür.
    """
    try:
        data = await request.json()
        message = data.get("message", "").strip() # Mesajın başındaki ve sonundaki boşlukları temizle

        if not message:
            return {"response": "Lütfen bir mesaj yazın."}

        logging.info(f"Kullanıcıdan gelen mesaj: {message}")
        response = handle_chat(message)
        logging.info(f"AI'dan dönen genel yanıt: {response}")
        return {"response": response}
    except Exception as e:
        logging.error(f"Chatbot endpoint'inde beklenmedik hata: {e}", exc_info=True)
        return {"response": "Sohbet servisinde beklenmedik bir hata oluştu. Lütfen daha sonra tekrar deneyin."}