# App - Orquestador Principal

app.py es el script coordinador del proyecto. Ejecuta scrapers de distintas tiendas (Scrapy, Selenium y BeautifulSoup), consolida sus resultados y guarda un archivo final resultados.csv.

## Dependencias
- Python 3.8 o superior
- Módulos de Python estándar: csv, subprocess, os, pathlib
- Scrapers locales importados desde el paquete scrapers
- Dependencias externas requeridas por los scrapers individuales (Selenium, BeautifulSoup, requests, Scrapy, etc.)

## Estructura y comportamiento clave

### Descripción general
El script `app.py` coordina la ejecución de todos los scrapers del proyecto y genera un archivo CSV con los resultados consolidados.

### Flujo general
1. Ejecuta el spider de Scrapy (`scrapy crawl dislicores`) para obtener los datos de Dislicores.
2. Lee el archivo intermedio `resultados_dislicores.csv`.
3. Si no existe, crea un resultado por defecto con valores “No encontrado”.
4. Llama a las funciones de scraping de las demás tiendas en este orden:
   - scrape_olimpica()
   - scrape_jumbo()
   - scrape_quindio()
   - scrape_lalicorera()
   - scrape_lalico()
5. Guarda todos los resultados en `resultados.csv`.

### Manejo de errores
- Captura excepciones al ejecutar subprocess.run()
- Maneja errores al leer y eliminar archivos CSV intermedios
- Si un archivo no existe, devuelve valores por defecto

### Mejores prácticas sugeridas
- Reemplazar `print()` por `logging`
- Ejecutar scrapers en paralelo (concurrent.futures)
- Normalizar precios a formato numérico
- Validar la estructura de salida

---

# Dislicores - Scrapy

Un scraper eficiente que extrae información de productos directamente desde la API de Dislicores usando Scrapy.

## Objetivo del proyecto
Extraer el nombre y precio del whisky Johnnie Walker Blue Label desde la tienda Dislicores usando su API pública.

## Diferencias clave
| Aspecto | Jumbo (Selenium) | Dislicores (Scrapy) |
|----------|------------------|---------------------|
| Método | Scraping de HTML | Consulta directa a API |
| Herramienta | Selenium | Scrapy |
| Navegador | Necesita Chrome | No necesita navegador |
| Velocidad | 5–8 segundos | 1–2 segundos |
| Complejidad | Alta | Baja |
| Recursos | 150–200 MB | 20–30 MB |

## Ventajas principales
- Rápido: no necesita renderizar páginas
- Confiable: menos propenso a cambios en el HTML
- Eficiente: bajo consumo de recursos

## Estructura general del código
```python
import scrapy
import json

class DislicoresSpider(scrapy.Spider):
    name = "dislicores"
    start_urls = ["https://www.dislicores.com/api/catalog_system/pub/products/search?ft=blue%20label"]
    
    def parse(self, response):
        data = json.loads(response.text)
        # procesamiento del JSON
```

## Flujo
1. Define la spider con `name = "dislicores"` y la URL de búsqueda.
2. Convierte la respuesta JSON a un diccionario de Python.
3. Recorre cada producto y busca coincidencias con “blue”.
4. Extrae el nombre y el precio desde la estructura del JSON.
5. Formatea el resultado:
   ```python
   {'tienda': 'Dislicores', 'producto': nombre.strip(), 'precio': f"${precio:,.0f}"}
   ```
6. Si no encuentra resultados, devuelve “No encontrado”.

---

# Jumbo - Selenium

Un scraper automatizado que extrae información de productos (nombre y precio) desde la página web de Jumbo Colombia usando Selenium.

## Objetivo
Extraer el precio total del whisky Johnnie Walker Blue Label desde Jumbo, evitando capturar el precio por mililitro.

## Flujo del código
1. Importa Selenium y configura Chrome con modo headless.
2. Carga la URL del producto.
3. Espera que cargue el JavaScript con `WebDriverWait`.
4. Cierra popups que interfieran.
5. Usa expresiones regulares para detectar el precio correcto.
6. Descarta precios por mililitro o por unidad.
7. Devuelve el resultado como diccionario:
   ```python
   {"tienda": "Jumbo", "producto": producto, "precio": precio}
   ```

## Conceptos utilizados
- Selenium WebDriver
- Headless Chrome
- WebDriverWait y expected_conditions
- Expresiones regulares
- Fallbacks y manejo de errores

---

# La Licorera - Selenium

`lalicorera_selenium.py` utiliza Selenium para extraer el nombre y el precio del Johnnie Walker Blue Label desde la tienda La Licorera.

## Descripción
Extrae el producto y el precio desde:
```
https://lalicorera.com/productos/whisky/johnnie-walker-blue-label
```

## Flujo
1. Configura Chrome con opciones headless.
2. Carga la URL del producto.
3. Espera los elementos:
   - `h1.svelte-1jgubmi` (nombre del producto)
   - `h2.price.svelte-1jgubmi` (precio)
4. Devuelve:
   ```python
   {"tienda": "La Licorera", "producto": "Johnnie Walker Blue Label 750ml", "precio": "$1.190.000"}
   ```

## Manejo de errores
- Captura excepciones durante la navegación.
- Devuelve “No encontrado” si los elementos no aparecen.
- Cierra el driver en bloque `finally`.

---

# Lalico - Selenium

`lalico_selenium.py` utiliza Selenium para obtener el nombre y el precio del Blue Label desde Lalico.

## Descripción
Extrae datos desde:
```
https://lalico.com.co/products/blue-label-750ml
```

## Flujo
1. Configura Chrome en modo headless.
2. Busca los elementos:
   - `h1.product-single__title[itemprop='name']`
   - `span.product-single__price[itemprop='price']`
3. Retorna:
   ```python
   {"tienda": "Lalico", "producto": "Johnnie Walker Blue Label 750ml", "precio": "$1.200.000"}
   ```

## Manejo de errores
- Controla excepciones durante la extracción.
- Cierra el navegador siempre con `finally`.
- Garantiza robustez ante errores de carga.

---

# Olímpica - BeautifulSoup

`olimpica_bs4.py` utiliza Requests y BeautifulSoup para extraer el nombre y precio del Johnnie Walker Blue Label desde Olímpica.

## Flujo
1. Solicita la página del producto con `requests.get()`.
2. Analiza el HTML con `BeautifulSoup`.
3. Busca múltiples selectores posibles para nombre y precio.
4. Usa expresiones regulares para limpiar y validar el precio.
5. Retorna el resultado como diccionario:
   ```python
   {"tienda": "Olímpica", "producto": "Johnnie Walker Blue Label 750ml", "precio": "$1.190.000"}
   ```

## Recomendaciones
- Manejar errores de red con `try/except`.
- Añadir reintentos automáticos.
- Incluir logging para trazabilidad.

---

# Quindío - BeautifulSoup

`quindio_bs4.py` usa Requests y BeautifulSoup para obtener nombre y precio del producto Blue Label desde la tienda Licores El Quindío.

## Flujo
1. Solicita la página:
   ```
   https://licoresquindio.com/producto/whisky-johnnie-walker-blue-label-750ml/
   ```
2. Parsea con BeautifulSoup.
3. Busca:
   - `h1.single-post-title.product_title.entry-title`
   - `span.woocommerce-Price-amount.amount`
4. Retorna:
   ```python
   {'tienda': 'Licores El Quindío', 'producto': 'Whisky Johnnie Walker Blue Label 750ml', 'precio': '$910.000'}
   ```

## Mejora sugerida
Agregar manejo de errores y timeout.
