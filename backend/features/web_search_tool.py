# features/web_search_tool.py

def get_fallback_search_link(query: str):
    """
    Kullanıcının yazdığı sorguya göre Zara, Bershka ya da genel Google arama linki döndürür.
    """
    q = query.lower()

    if "zara" in q:
        return f"https://www.zara.com/tr/tr/search?searchTerm={query.replace(' ', '+')}"
    elif "bershka" in q:
        return f"https://www.bershka.com/tr/search?q={query.replace(' ', '+')}"
    elif "stradivarius" in q:
        return f"https://www.stradivarius.com/tr/search?q={query.replace(' ', '+')}"
    elif "mango" in q:
        return f"https://shop.mango.com/tr/kadin/arama?q={query.replace(' ', '+')}"
    else:
        # Genel Google fallback
        return f"https://www.google.com/search?q={query.replace(' ', '+')}"
