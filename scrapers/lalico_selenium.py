from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def scrape_lalico(url="https://lalico.com.co/products/blue-label-750ml"):
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

        # Esperar por el título
        try:
            titulo_elem = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "h1.product-single__title[itemprop='name']"))
            )
            producto = titulo_elem.text.strip()
        except Exception:
            pass

        # Esperar por el precio
        try:
            precio_elem = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "span.product-single__price[itemprop='price']"))
            )
            precio = precio_elem.text.strip()
        except Exception:
            # Intenta selector alternativo por id
            try:
                precio_elem = driver.find_element(By.CSS_SELECTOR, "span[id^='ProductPrice']")
                precio = precio_elem.text.strip()
            except Exception:
                pass

        time.sleep(0.3)

    except Exception as e:
        print(f"Error en Lalico: {e}")
    finally:
        try:
            driver.quit()
        except Exception:
            pass

    return {"tienda": "Lalico", "producto": producto, "precio": precio}
