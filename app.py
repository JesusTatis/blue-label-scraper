import csv
import subprocess
import os
from pathlib import Path
import pandas as pd
from scrapers.jumbo_selenium import scrape_jumbo
from scrapers.quindio_bs4 import scrape_quindio

def scrape_dislicores():
    # Ejecuta el spider de Scrapy (genera resultados_dislicores.csv en la raíz del proyecto)
    try:
        subprocess.run(['scrapy', 'crawl', 'dislicores'], cwd='scrapers/dislicores_scrapy')
    except Exception as e:
        print(f"⚠️ Error ejecutando el spider de Dislicores: {e}")

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
        print(f"⚠️ Error leyendo {csv_path}: {e}")

    # Intentamos eliminar el CSV intermedio para que solo quede el resultados.csv final
    try:
        csv_path.unlink()
    except Exception as e:
        print(f"⚠️ No se pudo borrar {csv_path}: {e}")

    if results:
        return results
    return [{'tienda': 'Dislicores', 'producto': 'No encontrado', 'precio': 'No encontrado'}]

def guardar_csv(datos):
    # Guardar como XLSX usando pandas
    df = pd.DataFrame(datos)
    try:
        df.to_excel('resultados.xlsx', index=False, engine='openpyxl')
        print("\nDatos guardados en 'resultados.xlsx'")
    except Exception as e:
        # Fallback a CSV si no se puede escribir xlsx
        with open('resultados.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['tienda', 'producto', 'precio'])
            writer.writeheader()
            writer.writerows(datos)
        print(f"\nNo se pudo crear XLSX ({e}), se guardó 'resultados.csv' en su lugar.")

if __name__ == "__main__":
    print("Scrapeando datos de Blue Label...\n")
    resultados = []
    dislicores_rows = scrape_dislicores()
    # scrape_dislicores ahora devuelve una lista de filas
    if isinstance(dislicores_rows, list):
        resultados.extend(dislicores_rows)
    else:
        resultados.append(dislicores_rows)
    print("Dislicores listo")
    resultados.append(scrape_jumbo())
    print("Jumbo listo")
    resultados.append(scrape_quindio())
    print("Licores El Quindio listo")

    guardar_csv(resultados)
