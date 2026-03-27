# ============================================================
# LOAD.PY — LA CARGA (guardar el resultado final)
# ============================================================
# Ya cocinamos el plato (la Master Table).
# Ahora lo servimos en el plato (guardamos el CSV)
# y revisamos que todo quedo bien (reporte de calidad).
# ============================================================

import pandas as pd
import os

# Donde vamos a guardar el resultado
DATA_PROCESSED = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed')
# Traduce a: "la carpeta data/processed/ un nivel arriba de donde estoy"


# --- GUARDAR LA MASTER TABLE ---
def cargar_master_table(master_table):
    os.makedirs(DATA_PROCESSED, exist_ok=True)
    # Crea la carpeta si no existe. exist_ok=True = no explota si ya existe.

    outpath = os.path.join(DATA_PROCESSED, 'master_table.csv')
    # El archivo se va a llamar master_table.csv

    master_table.to_csv(outpath, index=False)
    # .to_csv() = exporta la tabla de pandas a un archivo CSV
    # index=False = no agrega una columna extra con numeros de fila

    print(f"\n[LOAD] Master Table guardada en: {outpath}")
    print(f"[LOAD] Filas: {master_table.shape[0]} | Columnas: {master_table.shape[1]}")
    # Confirma: 363 filas, 16 columnas
    return outpath


# --- REPORTE DE CALIDAD (revisar que todo quedo limpio) ---
def reporte_calidad(df_ga4, df_gads, df_meta, df_gsc_chart, df_gsc_queries, df_ventas, master):
    print("\n" + "=" * 60)
    print("REPORTE DE CALIDAD")
    print("=" * 60)

    datos = {
        'ga4': df_ga4, 'google_ads': df_gads, 'meta_ads': df_meta,
        'gsc_chart': df_gsc_chart, 'gsc_queries': df_gsc_queries,
        'ventas': df_ventas, 'master_table': master
    }
    # Mete todas las tablas en un diccionario {nombre: tabla}

    for nombre, df in datos.items():
        nulls = df.isnull().sum().sum()     # cuenta TODOS los valores vacios en toda la tabla
        dupes = df.duplicated().sum()       # cuenta filas repetidas
        print(f"  {nombre:15s} | Filas: {df.shape[0]:>6} | Cols: {df.shape[1]:>3} | Nulls: {nulls:>5} | Dupes: {dupes:>4}")
    # Para cada tabla imprime: nombre, filas, columnas, vacios, duplicados
    # Si todo salio bien: Nulls = 0 y Dupes = 0 en todas


# --- FUNCION PRINCIPAL: guarda y reporta ---
def cargar_todo(df_ga4, df_gads, df_meta, df_gsc_chart, df_gsc_queries, df_ventas, master):
    print("\n" + "=" * 60)
    print("ETAPA: CARGA")
    print("=" * 60)

    outpath = cargar_master_table(master)              # guarda el CSV
    reporte_calidad(df_ga4, df_gads, df_meta, df_gsc_chart, df_gsc_queries, df_ventas, master)
    # imprime el reporte de calidad

    print(f"\n[LOAD] Proceso de carga completado")
    return outpath
    # Devuelve la ruta donde quedo guardado el archivo
