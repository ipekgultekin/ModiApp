# features/search_products.py

import faiss
import json
import numpy as np
from sentence_transformers import SentenceTransformer

# Modeli yükle
model = SentenceTransformer("all-MiniLM-L6-v2")

# FAISS indexi ve ürünleri yükle
index = faiss.read_index("data/product_index.faiss")
with open("data/product_id_map.json", "r", encoding="utf-8") as f:
    products = json.load(f)

def search_similar_products(query, top_k=3):
    query_embedding = model.encode([query])
    distances, indices = index.search(np.array(query_embedding), top_k)

    results = []
    for idx in indices[0]:
        if idx < len(products):
            results.append(products[idx])
    return results
