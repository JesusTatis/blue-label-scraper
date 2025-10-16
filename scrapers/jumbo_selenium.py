from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_jumbo(url="https://www.jumbocolombia.com/whisky-johnnie-walker-blue-label-mini-cube-x-750-ml/p"):
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=options)
    driver.get(url)

    wait = WebDriverWait(driver, 7)

    producto = "No encontrado"
    precio = "No encontrado"

    try:
        # --- Nombre del producto ---
        try:
            nombre_elem = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "h1.vtex-store-components-3-x-productBrand"))
            )
            producto = nombre_elem.text.strip()
        except:
            try:
                producto = driver.find_element(By.TAG_NAME, "h1").text.strip()
            except:
                pass

        # --- Precio exacto ---
        try:
            price_elem = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "span.vtex-product-price-1-x-sellingPriceValue"))
            )
            precio = price_elem.text.strip()

            # Normalizamos el formato
            precio = precio.replace("\xa0", " ")  # elimina espacios invisibles
            if not precio.startswith("$"):
                precio = f"$ {precio}"
        except:
            # Si no aparece el span principal, buscar con JS como respaldo
            texto = driver.execute_script("return document.body.innerText;")
            for line in texto.split("\n"):
                if "$" in line and len(line) > 6:
                    precio = line.strip()
                    break

    except Exception as e:
        print(f"⚠️ Error en Jumbo: {e}")
    finally:
        driver.quit()

    return {"tienda": "Jumbo", "producto": producto, "precio": precio}


if __name__ == "__main__":
    print(scrape_jumbo())
