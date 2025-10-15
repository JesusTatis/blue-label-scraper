import scrapy

class DislicoresSpider(scrapy.Spider):
    name = "dislicores"
    start_urls = ["https://www.dislicores.com/search?q=blue+label"]

    def parse(self, response):
        producto = response.css('a.product-item-link::text').get()
        precio = response.css('span.price::text').get()
        yield {
            'tienda': 'Dislicores',
            'producto': producto.strip() if producto else 'No encontrado',
            'precio': precio.strip() if precio else 'No encontrado'
        }
