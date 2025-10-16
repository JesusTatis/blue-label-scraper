import scrapy
import json

class DislicoresSpider(scrapy.Spider):
    name = "dislicores"
    start_urls = ["https://www.dislicores.com/api/catalog_system/pub/products/search?ft=blue%20label"]

    def parse(self, response):
        data = json.loads(response.text)
        if not data:
            yield {
                'tienda': 'Dislicores',
                'producto': 'No encontrado',
                'precio': 'No encontrado'
            }
            return

        # Tomar el primer producto que contenga 'Blue Label' en el nombre
        for item in data:
            nombre = item.get('productName', 'No encontrado')
            if 'blue' in nombre.lower():
                precio = item.get('items', [{}])[0].get('sellers', [{}])[0].get('commertialOffer', {}).get('Price', 0)
                yield {
                    'tienda': 'Dislicores',
                    'producto': nombre.strip(),
                    'precio': f"${precio:,.0f}" if precio else 'No encontrado'
                }
                return

        # Si no encuentra ninguno
        yield {
            'tienda': 'Dislicores',
            'producto': 'No encontrado',
            'precio': 'No encontrado'
        }
