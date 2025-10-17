from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re

def scrape_jumbo(url="https://www.jumbocolombia.com/whisky-johnnie-walker-blue-label-mini-cube-x-750-ml/p"):
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")

    driver = webdriver.Chrome(options=options)
    driver.get(url)

    # Esperamos a que cargue el contenido
    time.sleep(3)

    producto = "No encontrado"
    precio = "No encontrado"

    try:
        # Nombre del producto
        try:
            nombre_elem = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "h1.vtex-store-components-3-x-productBrand"))
            )
            producto = nombre_elem.text.strip()
        except:
            try:
                producto = driver.find_element(By.TAG_NAME, "h1").text.strip()
            except:
                pass

        # Cerrar popups
        try:
            close_buttons = driver.find_elements(By.CSS_SELECTOR, "button[aria-label='Close'], .close")
            for btn in close_buttons:
                try:
                    btn.click()
                    time.sleep(0.5)
                except:
                    pass
        except:
            pass

        # NUEVA ESTRATEGIA: Buscar específicamente precios SIN "x ml"
        # El precio correcto NO tiene "x ml" o "ml" después
        # El precio por ml SÍ tiene "x ml" después
        
        try:
            # Obtenemos todo el texto de la página
            body_text = driver.find_element(By.TAG_NAME, "body").text
            
            # Buscamos todos los precios con regex
            # Patrón: $ seguido de números con puntos/comas
            patron_precio = r'\$\s*[\d.,]+'
            precios_encontrados = re.findall(patron_precio, body_text)
            
            # Filtramos y analizamos cada precio
            precios_validos = []
            for precio_texto in precios_encontrados:
                # Extraemos solo dígitos
                solo_digitos = re.sub(r'[^\d]', '', precio_texto)
                
                if len(solo_digitos) >= 6:  # Precio grande (más de 6 dígitos)
                    # Buscamos el contexto alrededor del precio en el texto
                    idx = body_text.find(precio_texto)
                    if idx != -1:
                        # Miramos los 10 caracteres después del precio
                        contexto = body_text[idx:idx + len(precio_texto) + 10].lower()
                        
                        # Si NO contiene "ml" o "x ml", es el precio total
                        if 'ml' not in contexto and 'x' not in contexto:
                            precios_validos.append({
                                'texto': precio_texto,
                                'digitos': len(solo_digitos),
                                'valor': int(solo_digitos)
                            })
            
            # Ordenamos por cantidad de dígitos (descendente)
            if precios_validos:
                precios_validos.sort(key=lambda x: x['digitos'], reverse=True)
                precio = precios_validos[0]['texto'].strip()
                
        except Exception as e:
            print(f"Error en estrategia de regex: {e}")

        # Plan B: Buscar con selectores CSS excluyendo elementos con "ml"
        if precio == "No encontrado":
            try:
                all_elements = driver.find_elements(By.CSS_SELECTOR, "span, div")
                
                for elem in all_elements:
                    texto = elem.text.strip()
                    
                    # Si contiene $ y números
                    if "$" in texto:
                        solo_digitos = re.sub(r'[^\d]', '', texto)
                        
                        # Debe tener 6+ dígitos Y NO contener "ml" o "x"
                        if (len(solo_digitos) >= 6 and 
                            'ml' not in texto.lower() and 
                            'x ml' not in texto.lower() and
                            len(texto) < 30):  # No debe ser un texto largo
                            
                            precio = texto.replace("\xa0", " ").strip()
                            break
                            
            except Exception as e:
                print(f"Error en Plan B: {e}")

        # Plan C: JavaScript avanzado
        if precio == "No encontrado":
            try:
                script = """
                let precios = [];
                document.querySelectorAll('*').forEach(el => {
                    let text = el.textContent.trim();
                    if (text.includes('$') && text.length < 30) {
                        let digitos = text.replace(/[^0-9]/g, '');
                        // Solo si tiene 6+ dígitos Y NO tiene "ml"
                        if (digitos.length >= 6 && !text.toLowerCase().includes('ml')) {
                            precios.push({
                                texto: text,
                                digitos: digitos.length
                            });
                        }
                    }
                });
                precios.sort((a, b) => b.digitos - a.digitos);
                return precios.length > 0 ? precios[0].texto : null;
                """
                resultado_js = driver.execute_script(script)
                if resultado_js:
                    precio = resultado_js.replace("\xa0", " ").strip()
            except Exception as e:
                print(f"Error en JavaScript: {e}")

    except Exception as e:
        print(f"Error en Jumbo: {e}")

    return {"tienda": "Jumbo", "producto": producto, "precio": precio}


if __name__ == "__main__":
    resultado = scrape_jumbo()
