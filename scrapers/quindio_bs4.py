import requests
from bs4 import BeautifulSoup

def scrape_quindio():
    url = "https://licoresquindio.com/producto/whisky-johnnie-walker-blue-label-750ml/"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    producto = soup.find('h1', {'class': 'single-post-title product_title entry-title'})
    precio = soup.find('span', {'class': 'woocommerce-Price-amount amount'})
    
    if producto and precio:
        return {'tienda': 'Licores El Quindio', 'producto': producto.text.strip(), 'precio': precio.text.strip()}
    else:
        return {'tienda': 'Licores El Quindio', 'producto': 'No encontrado', 'precio': 'No encontrado'}
