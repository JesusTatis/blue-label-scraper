from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def scrape_jumbo():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=options)

    url = "https://www.jumbocolombia.com/whisky-johnnie-walker-blue-label-mini-cube-x-750-ml/p"
    driver.get(url)
    driver.implicitly_wait(5)

    try:
        producto = driver.find_element("css selector", "a.vtex-product-summary-2-x-productBrand").text
        precio = driver.find_element("css selector", "span.vtex-product-price-1-x-sellingPriceValue").text
        resultado = {'tienda': 'Jumbo', 'producto': producto, 'precio': precio}
    except:
        resultado = {'tienda': 'Jumbo', 'producto': 'No encontrado', 'precio': 'No encontrado'}

    driver.quit()
    return resultado
