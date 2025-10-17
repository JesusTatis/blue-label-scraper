# Archivo: `app.py`

## Descripción

`app.py` es el script **coordinador** del proyecto. Ejecuta scrapers de distintas tiendas (Scrapy, Selenium y BeautifulSoup), consolida sus resultados y guarda un archivo final `resultados.csv`.

---

## Dependencias

- Python 3.8+
- Módulos de Python estándar: `csv`, `subprocess`, `os`, `pathlib`
- Scrapers locales importados desde el paquete `scrapers` (ver lista abajo)
- Externas requeridas por los scrapers individuales (Selenium, BeautifulSoup, requests, Scrapy, etc.)

---

## Estructura y comportamiento clave

### Imports (exactos en el código)

```python
from scrapers.jumbo_selenium import scrape_jumbo
from scrapers.quindio_bs4 import scrape_quindio
from scrapers.lalicorera_selenium import scrape_lalicorera
from scrapers.olimpica_bs4 import scrape_olimpica
from scrapers.lalico_selenium import scrape_lalico

```

### `scrape_dislicores()`

- Ejecuta el spider de Scrapy con:

```python
subprocess.run(['scrapy', 'crawl', 'dislicores'], cwd='scrapers/dislicores_scrapy')
```

- Busca el archivo `resultados_dislicores.csv` en la raíz del proyecto.
- Si no existe, devuelve una lista con un diccionario por defecto:

```python
[{'tienda': 'Dislicores', 'producto': 'No encontrado', 'precio': 'No encontrado'}]
```

- Si existe, lee el CSV con `csv.DictReader`, normaliza las claves `tienda`, `producto`, `precio` (si faltan usa los valores por defecto arriba), y devuelve la lista de filas como diccionarios.
- Intenta eliminar (`unlink()`) `resultados_dislicores.csv` al terminar (captura excepciones si falla).

### `guardar_csv(datos)`

- Recibe `datos` que puede contener listas y diccionarios anidados (estructura producida por la ejecución de los scrapers).
- Aplana los elementos (extrae diccionarios dentro de listas) y construye una lista `flat` de diccionarios.
- Determina dinámicamente todas las columnas/keys presentes en `flat`.
- Prioriza el orden de columnas: `tienda`, `producto`, `precio`. Añade luego cualquier otra clave que aparezca.
- Escribe `resultados.csv` en la raíz con `csv.DictWriter`, usando `encoding='utf-8'`.
- Imprime `"Datos guardados en 'resultados.csv'"` al finalizar.

### Bloque principal (`if __name__ == "__main__":`)

- Imprime `Scrapeando datos de Blue Label...`
- Ejecuta `scrape_dislicores()` y, si regresa lista, extiende `resultados`; si no, lo agrega.
- Llama a los scrapers en este orden **exacto** (tal como están en el código):
    1. `scrape_olimpica()`
    2. `scrape_jumbo()`
    3. `scrape_quindio()`
    4. `scrape_lalicorera()`
    5. `scrape_lalico()`
- Imprime una línea de confirmación (`✅... listo`) después de cada llamada.
- Finalmente llama a `guardar_csv(resultados)`.

---

## Entradas / Salidas

- Entrada: llamadas a funciones de los módulos `scrapers.*`. `scrape_dislicores()` depende de que el spider Scrapy genere `resultados_dislicores.csv`.
- Salida: `resultados.csv` en la raíz del proyecto con columnas detectadas dinámicamente (al menos `tienda`, `producto`, `precio`).

---

## Manejo de errores observado

- Captura excepciones alrededor de:
    - `subprocess.run(...)` — imprime error si falla.
    - Lectura del CSV intermedio — imprime error si hay problema leyendo.
    - Eliminación del CSV intermedio — imprime si no se puede borrar.
- Si `resultados_dislicores.csv` no existe devuelve un resultado por defecto para Dislicores.

---

## Buenas prácticas / mejoras sugeridas (opcionales)

- Usar `subprocess.run(..., check=True, capture_output=True)` para detectar errores y registrar salida de forma controlada.
- Convertir `print()` por el módulo `logging` (niveles INFO/ERROR).
- Normalizar formatos de precio (ej. número entero en `precio_cop`) en cada scraper antes de guardar.
- Validar que los scrapers devuelvan estructuras consistentes: siempre dicts con `tienda`, `producto`, `precio`.
- Manejar rutas con `Path(...).resolve()` para evitar problemas si el script se ejecuta desde otra carpeta.
- Considerar ejecución paralela de scrapers si el tiempo es crítico (`concurrent.futures`).

---

## Ejemplo de uso

Ejecutar desde la raíz del proyecto:

```bash
python app.py
```


# Lalico - Selenium

# Archivo: `lalico_selenium.py`

## Descripción

`lalico_selenium.py` es un módulo que utiliza **Selenium** para extraer el **nombre** y el **precio** del producto (por defecto la página de Blue Label 750ml) desde `https://lalico.com.co/products/blue-label-750ml`.

---

## Dependencias

- `selenium` (webdriver, Options, By, WebDriverWait, expected_conditions)
- `time` (sleep)
- Un ChromeDriver compatible con la versión de Chrome instalada

---

## Función pública

```python
def scrape_lalico(url="https://lalico.com.co/products/blue-label-750ml"):
    ...
    return {"tienda": "Lalico", "producto": producto, "precio": precio}

```

### Parámetros

- `url` (opcional): URL del producto. Si no se pasa, usa la URL por defecto del Blue Label indicada arriba.

### Flujo y selectores

1. Configura `Options()` con estos argumentos (tal como en el código):
    - `-headless=new`
    - `-disable-gpu`
    - `-no-sandbox`
    - `-disable-dev-shm-usage`
    - `-window-size=1920,1080`
    - `-disable-blink-features=AutomationControlled`
    - `user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36`
2. Inicia `webdriver.Chrome(options=options)`.
3. `driver.get(url)`
4. Espera por el título del producto con:
    
    ```css
    h1.product-single__title[itemprop='name']
    
    ```
    
    Si aparece, asigna su texto a `producto`.
    
5. Espera por el precio con:
    
    ```css
    span.product-single__price[itemprop='price']
    
    ```
    
    Si no aparece, intenta un selector alternativo por id:
    
    ```css
    span[id^='ProductPrice']
    
    ```
    
6. `time.sleep(0.3)` para asegurar carga mínima antes de cerrar.
7. Asegura cerrar el driver en `finally` con `driver.quit()` (captura excepciones al cerrar).

---

## Salida

- Devuelve un diccionario con las claves exactas:

```python
{"tienda": "Lalico", "producto": <str| "No encontrado">, "precio": <str| "No encontrado">}

```

- `producto` y `precio` serán `"No encontrado"` si no se localizan los selectores.

---

## Manejo de errores

- Captura errores generales en la carga y extracción; imprime `Error en Lalico: {e}` si ocurre una excepción.
- Garantiza `driver.quit()` en el bloque `finally` aunque falle algo (captura excepción al cerrar).

---

## Notas / recomendaciones

- `-headless=new` es la opción de Chrome más reciente; verificar compatibilidad con la versión de ChromeDriver.
- Si se requiere mayor robustez, transformar la lógica para:
    - Recibir `timeout` como parámetro para `WebDriverWait`.
    - Registrar errores via `logging`.
    - Retornar además un campo `precio_cop` con la conversión numérica (si se desea análisis cuantitativo).
- Mantener actualizado el `user-agent` si el sitio bloquea agentes inusuales.

---

## Ejemplo de retorno esperado

```python
{"tienda": "Lalico", "producto": "Johnnie Walker Blue Label 750ml", "precio": "$ 1.200.000"}
```

(El formato exacto del `precio` depende de cómo lo muestre la página en el selector encontrado.)

Salida esperada (consola): mensajes de progreso y creación de `resultados.csv`.

---
