# embed_products.py
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# 1. Modeli yükle
model = SentenceTransformer('all-MiniLM-L6-v2')

# 2. JSON dosyasını oku
with open('data/products.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

# 3. Description'ları al
descriptions = [product['description'] for product in products]

# 4. Vektörle
embeddings = model.encode(descriptions)

# 5. FAISS veritabanı oluştur
dimension = embeddings[0].shape[0]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings))

# 6. Veritabanını kaydet
faiss.write_index(index, 'data/product_index.faiss')

# 7. Mapping için ID'leri ayrı kaydet (ID ile ürün eşleştirme)
with open('data/product_id_map.json', 'w', encoding='utf-8') as f:
    json.dump(products, f, ensure_ascii=False, indent=2)

print("✅ Ürünler başarıyla vektörlendi ve veritabanı oluşturuldu.")
