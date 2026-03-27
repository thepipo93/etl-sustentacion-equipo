# ============================================================
# EXTRACT.PY — LA EXTRACCION (ir a buscar los datos)
# ============================================================
# Esto es como ir al supermercado y traer 5 bolsas diferentes.
# Cada bolsa es una fuente de datos distinta.
# No tocamos nada, solo los traemos como estan.
# ============================================================

import pandas as pd          # pandas = la herramienta para leer tablas (como Excel pero en codigo)
import os                     # os = para encontrar archivos en el computador

# Aqui le decimos DONDE estan los archivos crudos (sin tocar)
DATA_RAW = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw')
# Traduce a: "ve a la carpeta data/raw/ que esta un nivel arriba de donde estoy"


# --- BOLSA 1: Google Analytics 4 (las visitas al sitio web) ---
def extraer_ga4():
    path = os.path.join(DATA_RAW, 'ga4_2025.csv')     # donde esta el archivo
    df = pd.read_csv(path, dtype={'fecha': str})       # leelo como tabla, la fecha dejala como texto por ahora
    print(f"[EXTRACT] GA4: {df.shape[0]} filas, {df.shape[1]} columnas")  # avisa cuantas filas trajo
    return df                                           # devuelve la tabla al que la pidio
    # shape[0] = filas (7,446), shape[1] = columnas
    # Este CSV vino de BigQuery (la base de datos de Google en la nube)


# --- BOLSA 2: Google Ads (la publicidad pagada en Google) ---
def extraer_google_ads():
    path = os.path.join(DATA_RAW, 'google_ads_2025.csv')
    df = pd.read_csv(path)                              # lee el archivo CSV y lo convierte en tabla
    print(f"[EXTRACT] Google Ads: {df.shape[0]} filas, {df.shape[1]} columnas")
    return df
    # 1,219 filas — cada fila es un dia de una campana con su inversion, clics, impresiones


# --- BOLSA 3: Meta Ads (la publicidad en Facebook/Instagram) ---
def extraer_meta_ads():
    path = os.path.join(DATA_RAW, 'meta_ads_2025.csv')
    df = pd.read_csv(path)
    print(f"[EXTRACT] Meta Ads: {df.shape[0]} filas, {df.shape[1]} columnas")
    return df
    # 26 filas — datos mensuales por campana (trafico, conversiones, alcance, mensajes)


# --- BOLSA 4: Google Search Console (las busquedas organicas, sin pagar) ---
def extraer_gsc():
    chart_path = os.path.join(DATA_RAW, 'gsc_chart_2025.csv')     # clics e impresiones por dia
    queries_path = os.path.join(DATA_RAW, 'gsc_queries_2025.csv')  # que palabras busca la gente
    df_chart = pd.read_csv(chart_path)       # 335 filas
    df_queries = pd.read_csv(queries_path)   # 996 filas
    print(f"[EXTRACT] GSC Chart: {df_chart.shape[0]} filas | Queries: {df_queries.shape[0]} filas")
    return df_chart, df_queries              # devuelve DOS tablas (por eso retorna dos cosas)


# --- BOLSA 5: Ventas (cada poliza vendida) ---
def extraer_ventas():
    path = os.path.join(DATA_RAW, 'ventas_2025.csv')
    df = pd.read_csv(path)
    print(f"[EXTRACT] Ventas: {df.shape[0]} filas, {df.shape[1]} columnas")
    return df
    # 1,011 filas — cada fila es una poliza vendida con fecha, producto y monto en Quetzales


# --- FUNCION PRINCIPAL: trae TODAS las bolsas de una vez ---
def extraer_todo():
    print("=" * 60)
    print("ETAPA: EXTRACCION")
    print("=" * 60)

    df_ga4 = extraer_ga4()                             # bolsa 1
    df_gads = extraer_google_ads()                     # bolsa 2
    df_meta = extraer_meta_ads()                       # bolsa 3
    df_gsc_chart, df_gsc_queries = extraer_gsc()       # bolsa 4 (viene en dos partes)
    df_ventas = extraer_ventas()                       # bolsa 5

    print(f"\n[EXTRACT] Extraccion completa: 5 fuentes cargadas")

    return df_ga4, df_gads, df_meta, df_gsc_chart, df_gsc_queries, df_ventas
    # Devuelve las 6 tablas (5 fuentes, pero GSC son 2 tablas)
    # Esto se lo pasa a transform.py para que las limpie
