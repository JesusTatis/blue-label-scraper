import csv
import subprocess
import os
from pathlib import Path
from scrapers.jumbo_selenium import scrape_jumbo
from scrapers.quindio_bs4 import scrape_quindio
from scrapers.lalicorera_selenium import scrape_lalicorera
from scrapers.olimpica_bs4 import scrape_olimpica
from scrapers.lalico_selenium import scrape_lalico

def scrape_dislicores():
    # Ejecuta el spider de Scrapy (genera resultados_dislicores.csv en la raíz del proyecto)
    try:
        subprocess.run(['scrapy', 'crawl', 'dislicores'], cwd='scrapers/dislicores_scrapy')
    except Exception as e:
        print(f" Error ejecutando el spider de Dislicores: {e}")

    csv_path = Path('resultados_dislicores.csv')
    results = []

    if not csv_path.exists():
        # Si no hay CSV, devolvemos una fila por defecto
        return [{'tienda': 'Dislicores', 'producto': 'No encontrado', 'precio': 'No encontrado'}]

    try:
        with csv_path.open(newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                results.append({
                    'tienda': row.get('tienda', 'Dislicores').strip() if row.get('tienda') else 'Dislicores',
                    'producto': row.get('producto', 'No encontrado').strip() if row.get('producto') else 'No encontrado',
                    'precio': row.get('precio', 'No encontrado').strip() if row.get('precio') else 'No encontrado'
                })
    except Exception as e:
        print(f" Error leyendo {csv_path}: {e}")

    # Intentamos eliminar el CSV intermedio para que solo quede el resultados.csv final
    try:
        csv_path.unlink()
    except Exception as e:
        print(f" No se pudo borrar {csv_path}: {e}")

    if results:
        return results
    return [{'tienda': 'Dislicores', 'producto': 'No encontrado', 'precio': 'No encontrado'}]

def guardar_csv(datos):
    flat = []
    for item in datos:
        if isinstance(item, list):
            for sub in item:
                if isinstance(sub, dict):
                    flat.append(sub)
        elif isinstance(item, dict):
            flat.append(item)
        else:
            pass

    # Determinar dinámicamente todas las columnas presentes
    all_keys = []
    for row in flat:
        if isinstance(row, dict):
            for k in row.keys():
                if k not in all_keys:
                    all_keys.append(k)

    # Asegurar orden preferente: tienda, producto, precio
    preferred = ['tienda', 'producto', 'precio']
    fieldnames = [k for k in preferred if k in all_keys]
    # Añadir el resto de claves en el orden en que aparecieron
    for k in all_keys:
        if k not in fieldnames:
            fieldnames.append(k)

    # Guardar a CSV con las columnas detectadas
    with open('resultados.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(flat)
    print("Datos guardados en 'resultados.csv'")

if __name__ == "__main__":
    print("Scrapeando datos de Blue Label...\n")
    resultados = []
    dislicores_rows = scrape_dislicores()
    if isinstance(dislicores_rows, list):
        resultados.extend(dislicores_rows)
    else:
        resultados.append(dislicores_rows)
    print("Dislicores listo")
    resultados.append(scrape_olimpica())
    print("✅Olímpica listo")
    resultados.append(scrape_jumbo())
    print("✅Jumbo listo")
    resultados.append(scrape_quindio())
    print("✅Licores El Quindio listo")
    resultados.append(scrape_lalicorera())
    print("✅La Licorera listo")
    resultados.append(scrape_lalico())
    print("✅Lalico listo")

    guardar_csv(resultados)
