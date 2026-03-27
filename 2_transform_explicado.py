# ============================================================
# TRANSFORM.PY — LA TRANSFORMACION (limpiar y unir los datos)
# ============================================================
# Esto es como recibir las 5 bolsas del supermercado,
# lavar las frutas, pelar las verduras, cortar todo parejo
# y servir UN SOLO plato con todo combinado = la Master Table.
# ============================================================

import pandas as pd


# --- LAVAR BOLSA 1: Google Analytics 4 ---
def limpiar_ga4(df):
    df = df.copy()                                      # copia para no danar el original

    df['fecha'] = pd.to_datetime(df['fecha'], format='%Y%m%d', errors='coerce')
    # La fecha viene como "20250315" (texto pegado) → la convierte a 2025-03-15 (fecha real)
    # errors='coerce' = si alguna fecha esta rara, ponle NaT (vacio) en vez de explotar

    for col in ['eventos', 'usuarios', 'sesiones', 'pageviews', 'nuevos_usuarios']:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
    # Asegura que los numeros sean numeros (a veces vienen como texto)
    # fillna(0) = si hay un vacio, ponle 0
    # astype(int) = que sea numero entero, sin decimales

    df = df.drop_duplicates()                           # borra filas repetidas
    print(f"[TRANSFORM] GA4 limpio: {df.shape[0]} filas, nulls: {df.isnull().sum().sum()}")
    return df


# --- LAVAR BOLSA 2: Google Ads ---
def limpiar_google_ads(df):
    df = df.copy()

    df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')
    # Convierte la fecha a formato que Python entiende

    for col in ['impressions', 'clicks']:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
    # Impresiones y clics son numeros enteros

    for col in ['cost', 'conversions', 'ctr', 'avg_cpc']:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0.0)
    # Costos y conversiones pueden tener decimales (0.0)

    df['cpm'] = df.apply(
        lambda r: (r['cost'] / r['impressions'] * 1000) if r['impressions'] > 0 else 0, axis=1
    )
    # CPM = Costo Por Mil impresiones = (cuanto gaste / cuantas veces se mostro) * 1000
    # Si no se mostro (0 impresiones), el CPM es 0 para no dividir entre cero

    df = df.drop_duplicates()
    print(f"[TRANSFORM] Google Ads limpio: {df.shape[0]} filas, nulls: {df.isnull().sum().sum()}")
    return df


# --- LAVAR BOLSA 3: Meta Ads ---
def limpiar_meta_ads(df):
    df = df.copy()

    df['fecha_inicio'] = pd.to_datetime(df['date_start'], errors='coerce')
    df['fecha_fin'] = pd.to_datetime(df['date_stop'], errors='coerce')
    # Meta usa "date_start" y "date_stop" en ingles → los renombramos

    for col in ['impressions', 'clicks', 'reach', 'results']:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)

    for col in ['spend', 'cpm', 'cpc', 'ctr', 'frequency', 'cost_per_result']:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0.0)

    df = df.drop_duplicates()
    print(f"[TRANSFORM] Meta Ads limpio: {df.shape[0]} filas, nulls: {df.isnull().sum().sum()}")
    return df


# --- LAVAR BOLSA 4: Google Search Console ---
def limpiar_gsc(df_chart, df_queries):
    df_chart = df_chart.copy()

    df_chart['Date'] = pd.to_datetime(df_chart['Date'], errors='coerce')
    df_chart.rename(columns={
        'Date': 'fecha', 'Clicks': 'clicks',
        'Impressions': 'impressions', 'CTR': 'ctr', 'Position': 'position'
    }, inplace=True)
    # rename = cambiar los nombres de las columnas de ingles a minusculas
    # Para que cuando hagamos el merge, todas digan "fecha" igual

    if df_chart['ctr'].dtype == object:
        df_chart['ctr'] = df_chart['ctr'].str.rstrip('%').astype(float) / 100
    # Si el CTR viene como "4.5%" (texto), le quita el % y lo convierte a 0.045 (numero)

    df_queries = df_queries.copy()
    df_queries.rename(columns={
        'Top queries': 'query', 'Clicks': 'clicks',
        'Impressions': 'impressions', 'CTR': 'ctr', 'Position': 'position'
    }, inplace=True)
    if df_queries['ctr'].dtype == object:
        df_queries['ctr'] = df_queries['ctr'].str.rstrip('%').astype(float) / 100

    print(f"[TRANSFORM] GSC limpio: Chart {df_chart.shape[0]} filas | Queries {df_queries.shape[0]} filas")
    return df_chart, df_queries


# --- LAVAR BOLSA 5: Ventas ---
def limpiar_ventas(df):
    df = df.copy()

    df['fecha'] = pd.to_datetime(df['FECINIVIG'], errors='coerce')
    # La columna original se llama FECINIVIG (fecha inicio vigencia) → la renombramos a "fecha"

    df['monto'] = pd.to_numeric(df['MTOOPER'], errors='coerce').fillna(0.0)
    # MTOOPER = monto de la operacion en Quetzales guatemaltecos

    df = df.drop_duplicates()
    print(f"[TRANSFORM] Ventas limpio: {df.shape[0]} filas, nulls: {df.isnull().sum().sum()}")
    return df


# ============================================================
# CONSTRUIR LA MASTER TABLE (el plato final con todo junto)
# ============================================================
def construir_master_table(df_ga4, df_gads, df_gsc_chart, df_ventas):

    # --- Paso 1: agrupar cada fuente POR DIA ---
    # Porque puede haber varias filas por dia (varias campanas, varias paginas)
    # y necesitamos UNA fila por dia

    ga4_diario = df_ga4.groupby('fecha').agg(
        ga4_sesiones=('sesiones', 'sum'),        # suma todas las sesiones del dia
        ga4_usuarios=('usuarios', 'sum'),        # suma todos los usuarios del dia
        ga4_pageviews=('pageviews', 'sum'),      # suma todas las paginas vistas
        ga4_nuevos=('nuevos_usuarios', 'sum')    # suma los usuarios nuevos
    ).reset_index()
    # groupby('fecha') = agrupa las filas que tienen la misma fecha
    # .agg() = que operacion hacer con cada columna (sum = sumar)
    # reset_index() = que "fecha" vuelva a ser una columna normal

    gads_diario = df_gads.groupby('fecha').agg(
        gads_impressions=('impressions', 'sum'),
        gads_clicks=('clicks', 'sum'),
        gads_cost=('cost', 'sum'),
        gads_conversions=('conversions', 'sum')
    ).reset_index()

    # Calcular KPIs de Google Ads por dia
    gads_diario['gads_cpm'] = gads_diario.apply(
        lambda r: (r['gads_cost'] / r['gads_impressions'] * 1000) if r['gads_impressions'] > 0 else 0, axis=1
    )
    # CPM = cuanto cuesta que 1,000 personas vean tu anuncio

    gads_diario['gads_cpc'] = gads_diario.apply(
        lambda r: (r['gads_cost'] / r['gads_clicks']) if r['gads_clicks'] > 0 else 0, axis=1
    )
    # CPC = cuanto cuesta cada clic

    gads_diario['gads_cpa'] = gads_diario.apply(
        lambda r: (r['gads_cost'] / r['gads_conversions']) if r['gads_conversions'] > 0 else 0, axis=1
    )
    # CPA = cuanto cuesta cada conversion (alguien que hizo lo que querias: compro, se registro, etc.)

    # GSC ya viene por dia, solo renombramos
    gsc_diario = df_gsc_chart[['fecha', 'clicks', 'impressions']].copy()
    gsc_diario.rename(columns={'clicks': 'gsc_clicks', 'impressions': 'gsc_impressions'}, inplace=True)

    # Ventas agrupadas por dia
    ventas_diario = df_ventas.groupby('fecha').agg(
        ventas_cantidad=('NUMPOL', 'count'),     # cuenta cuantas polizas se vendieron ese dia
        ventas_monto=('monto', 'sum')            # suma el monto total vendido ese dia
    ).reset_index()

    # --- Paso 2: MERGE = unir todas las tablas por la columna "fecha" ---
    master = ga4_diario.merge(gads_diario, on='fecha', how='outer')
    # merge = unir dos tablas por una columna en comun
    # on='fecha' = la columna que tienen en comun
    # how='outer' = incluir TODOS los dias aunque una fuente no tenga datos ese dia

    master = master.merge(gsc_diario, on='fecha', how='outer')
    master = master.merge(ventas_diario, on='fecha', how='outer')
    # Cada merge agrega mas columnas a la tabla

    master = master.sort_values('fecha').reset_index(drop=True)
    # Ordena por fecha de enero a diciembre

    master = master.fillna(0)
    # Si algun dia no tiene datos de alguna fuente, pone 0 en vez de vacio

    print(f"\n[TRANSFORM] Master Table: {master.shape[0]} filas, {master.shape[1]} columnas")
    # Resultado: 363 filas (dias) x 16 columnas (metricas de todas las fuentes)
    return master


# --- FUNCION PRINCIPAL: limpia todo y construye la master table ---
def transformar_todo(df_ga4, df_gads, df_meta, df_gsc_chart, df_gsc_queries, df_ventas):
    print("\n" + "=" * 60)
    print("ETAPA: TRANSFORMACION")
    print("=" * 60)

    df_ga4 = limpiar_ga4(df_ga4)                       # lava bolsa 1
    df_gads = limpiar_google_ads(df_gads)              # lava bolsa 2
    df_meta = limpiar_meta_ads(df_meta)                # lava bolsa 3
    df_gsc_chart, df_gsc_queries = limpiar_gsc(df_gsc_chart, df_gsc_queries)  # lava bolsa 4
    df_ventas = limpiar_ventas(df_ventas)              # lava bolsa 5
    master = construir_master_table(df_ga4, df_gads, df_gsc_chart, df_ventas)  # cocina el plato

    return df_ga4, df_gads, df_meta, df_gsc_chart, df_gsc_queries, df_ventas, master
    # Devuelve las 6 tablas limpias + la master table (7 cosas en total)
    # Esto se lo pasa a load.py para que lo guarde
