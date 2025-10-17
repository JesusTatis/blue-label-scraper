
import re
import requests
from bs4 import BeautifulSoup

def scrape_olimpica(url="https://www.olimpica.com/whisky-johnnie-walker-blue-750-ml-5000267114279-829131/p"):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }
    r = requests.get(url, headers=headers, timeout=20)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")

    name_el = soup.select_one("span.vtex-store-components-3-x-productBrand") or \
              soup.select_one("span[class*='productBrand']") or \
              soup.find(["h1","h2"], string=re.compile("Blue", re.I))
    name = name_el.get_text(strip=True) if name_el else "No encontrado"

    # Intento de extraer volumen (ml) desde el título
    volume_ml = None
    m = re.search(r"(\d{2,4})\s?m?l", name, flags=re.I)
    if m:
        try:
            volume_ml = int(m.group(1))
        except Exception:
            volume_ml = None

    # Precio
    price_container = soup.select_one("span[class*='currencyContainer']")
    price_formatted = "No encontrado"
    price_numeric = None

    if price_container:
        raw = "".join(list(price_container.stripped_strings))
        raw = raw.replace("\xa0", "").replace(" ", "")
        price_formatted = raw
        digits = re.sub(r"[^\d]", "", raw)
        if digits:
            try:
                price_numeric = int(digits)
            except Exception:
                price_numeric = None

    if price_numeric is None:
        txt = soup.get_text(" ", strip=True)
        m2 = re.search(r"\$\s?\d{1,3}(?:\.\d{3})+", txt)
        if m2:
            price_formatted = re.sub(r"\s+", "", m2.group(0))
            digits = re.sub(r"[^\d]", "", price_formatted)
            try:
                price_numeric = int(digits)
            except Exception:
                price_numeric = None

    if price_numeric is None or price_formatted == "No encontrado":
        price_candidates = []
        price_pattern = re.compile(r"\$\s?[\d\.,]+")
        for el in soup.find_all(text=True):
            txt = el.strip()
            if not txt:
                continue
            m = price_pattern.search(txt)
            if m:
                candidate = re.sub(r"\s+", "", m.group(0))
                price_candidates.append(candidate)

        if price_candidates:
            price_formatted = price_candidates[0]
            digits = re.sub(r"[^\d]", "", price_formatted)
            try:
                price_numeric = int(digits)
            except Exception:
                price_numeric = None
                
    precio_texto = price_formatted if price_formatted else "No encontrado"
    precio_cop = price_numeric if price_numeric is not None else "No encontrado"

    return {
        "tienda": "Olímpica",
        "producto": name,
        "precio": precio_texto
    }
