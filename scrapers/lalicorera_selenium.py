from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def scrape_lalicorera(url="https://lalicorera.com/productos/whisky/johnnie-walker-blue-label?srsltid=AfmBOoolwoFpgJFAuwAx_guffHFpUjheizbHz77o6aqc5C3T4Ql_ItHm"):
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")

    driver = webdriver.Chrome(options=options)
    producto = "No encontrado"
    precio = "No encontrado"

    try:
        driver.get(url)

        # Esperar a que el título y el precio estén presentes
        try:
            titulo_elem = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "h1.svelte-1jgubmi"))
            )
            producto = titulo_elem.text.strip()
        except Exception:
            # si no aparece, seguimos
            pass

        try:
            precio_elem = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "h2.price.svelte-1jgubmi"))
            )
            precio = precio_elem.text.strip()
        except Exception:
            pass

        # Pequeña espera para asegurar que todo cargue si fuese necesario
        time.sleep(0.5)

    except Exception as e:
        print(f"Error en LaLicorera: {e}")
    finally:
        try:
            driver.quit()
        except Exception:
            pass

    return {"tienda": "La Licorera", "producto": producto, "precio": precio}
