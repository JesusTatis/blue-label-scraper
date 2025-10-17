import csv
import subprocess
import os
from pathlib import Path
from scrapers.jumbo_selenium import scrape_jumbo
from scrapers.quindio_bs4 import scrape_quindio

def scrape_dislicores():
    # Ejecuta el spider de Scrapy (genera resultados_dislicores.csv en la raíz del proyecto)
    subprocess.run(['scrapy', 'crawl', 'dislicores'], cwd='scrapers/dislicores_scrapy')
    with open('resultados_dislicores.csv', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            return row
    return {'tienda': 'Dislicores', 'producto': 'No encontrado', 'precio': 'No encontrado'}

def guardar_csv(datos):
    with open('resultados.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['tienda', 'producto', 'precio'])
        writer.writeheader()
        writer.writerows(datos)
    print("\n📄 Datos guardados en 'resultados.csv'")

if __name__ == "__main__":
    print("🕷️ Scrapeando datos de Blue Label...\n")
    resultados = []
    resultados.append(scrape_dislicores())
    print("✅ Dislicores listo")
    resultados.append(scrape_jumbo())
    print("✅ Jumbo listo")
    resultados.append(scrape_quindio())
    print("✅ Licores El Quindio listo")

    guardar_csv(resultados)
