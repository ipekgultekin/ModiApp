# agents/fallback_agent.py

from backend.features.search_products import search_similar_products
from backend.features.web_search_tool import get_fallback_search_link

def fallback_agent(query: str):
    """
    Kullanıcı sorgusuna göre önce FAISS'te arama yapar.
    Eğer sonuç bulunamazsa fallback olarak web linki döner.
    """
    results = search_similar_products(query)

    if results:
        return {
            "type": "vector_result",
            "data": results  # Bu ürünler RAG sistemine verilir
        }
    else:
        fallback_url = get_fallback_search_link(query)
        return {
            "type": "fallback_link",
            "url": fallback_url  # Bu doğrudan kullanıcıya gösterilir
        }
