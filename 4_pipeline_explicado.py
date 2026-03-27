# ============================================================
# PIPELINE.PY — EL ORQUESTADOR (el director de orquesta)
# ============================================================
# Este archivo NO hace nada por si solo.
# Solo LLAMA a los otros 3 en orden:
#   1. extract.py  → trae los datos
#   2. transform.py → los limpia y une
#   3. load.py → guarda el resultado
# Es como el mesero: no cocina, pero sabe el orden del servicio.
# ============================================================
# PARA CORRERLO: python src/pipeline.py
# ============================================================

import time                              # para medir cuanto tarda
from extract import extraer_todo         # trae la funcion de extraer
from transform import transformar_todo   # trae la funcion de transformar
from load import cargar_todo             # trae la funcion de cargar


def main():
    print("*" * 60)
    print("  PIPELINE ETL — Publicidad Digital Cliente_A (2025)")
    print("*" * 60)

    start = time.time()                  # empieza el cronometro

    # =============================================
    # PASO 1: EXTRACCION (la E de ETL)
    # =============================================
    # Llama a extract.py → lee los 6 CSVs crudos
    # Devuelve 6 tablas (DataFrames) sin tocar
    df_ga4, df_gads, df_meta, df_gsc_chart, df_gsc_queries, df_ventas = extraer_todo()

    # =============================================
    # PASO 2: TRANSFORMACION (la T de ETL)
    # =============================================
    # Llama a transform.py → limpia las 6 tablas y las une en UNA sola
    # Recibe 6 tablas crudas, devuelve 6 limpias + 1 master table = 7
    df_ga4, df_gads, df_meta, df_gsc_chart, df_gsc_queries, df_ventas, master = transformar_todo(
        df_ga4, df_gads, df_meta, df_gsc_chart, df_gsc_queries, df_ventas
    )

    # =============================================
    # PASO 3: CARGA (la L de ETL)
    # =============================================
    # Llama a load.py → guarda la master table como CSV + reporte de calidad
    outpath = cargar_todo(df_ga4, df_gads, df_meta, df_gsc_chart, df_gsc_queries, df_ventas, master)

    elapsed = time.time() - start        # para el cronometro
    print("\n" + "*" * 60)
    print(f"  PIPELINE COMPLETADO en {elapsed:.1f} segundos")    # 0.4 segundos
    print(f"  Archivo generado: {outpath}")                       # data/processed/master_table.csv
    print("*" * 60)


if __name__ == '__main__':      # si corres ESTE archivo directamente (no si lo importas)
    main()                      # ejecuta todo el pipeline
