# backend/app/agents/agent_main.py
from backend.features.ai_chat import generate_brand_search_link
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("models/gemini-1.5-flash-latest")
chat = model.start_chat(history=[])

query = input("Ne arıyorsunuz? ")

prompt = (
    f"Bir kullanıcı senden '{query}' ürünü için öneri istiyor. "
    f"Zara veya Bershka'da yoksa Mango, Stradivarius, Pull&Bear gibi benzer markalardan öneri üret. "
    f"Yalnızca ürün adı ve marka ver. Fiyat, açıklama veya link verme.\n\n"
    f"Yanıt formatı:\n"
    f"Siyah Elbise - Marka: Zara"
)

response = chat.send_message(prompt)
raw_lines = response.text.strip().split("\n")

print("\n🤖 AI Önerisi:\n")

for line in raw_lines:
    if " - Marka:" not in line:
        print(line)
        continue

    try:
        product, brand = line.split(" - Marka:")
        product = product.strip()
        brand = brand.strip()
        link = generate_brand_search_link(product, brand)
        print(f"🛍️ {product} - Marka: {brand}\n🔗 {link}\n")
    except Exception as e:
        print(f"{line} ❌ Hata: {e}")
