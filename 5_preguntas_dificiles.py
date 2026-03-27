# ============================================================
# PREGUNTAS DIFICILES DEL PROFE (basado en clase 26 marzo)
# ============================================================
# Estas son las preguntas que el profe hizo ayer a otros equipos
# y las que probablemente haga manana. Respuestas listas.
# ============================================================


# ── PREGUNTA: "Que hace el cursor?" ──────────────────────────
# Un cursor es un PUNTERO que ejecuta comandos SQL en la base de datos.
# Es como un dedo que senala fila por fila.
# En pandas seria como hacer iterrows().
#
# cursor = conn.cursor()        ← crea el puntero
# cursor.execute("CREATE...")   ← ejecuta un comando SQL
# cursor.executemany(query, data)  ← ejecuta el mismo comando para MUCHAS filas de un golpe
#
# Sin el cursor no puedes hablar con la base de datos.


# ── PREGUNTA: "Que hace executemany?" ────────────────────────
# executemany mete TODAS las filas del DataFrame de un solo golpe.
# En vez de hacer un INSERT por cada fila (lento), hace uno para todas (rapido).
#
# cursor.executemany(insert_query, data)
#   insert_query = "INSERT INTO tabla (col1, col2) VALUES (%s, %s)"
#   data = [(val1, val2), (val1, val2), ...]  ← lista de tuplas
#
# Los %s son PLACEHOLDERS (huecos) que se llenan con los valores reales.
# Es mejor practica que poner valores fijos porque es DINAMICO.


# ── PREGUNTA: "Que hace commit?" ─────────────────────────────
# conn.commit() CONFIRMA la transaccion.
# Sin commit, la base de datos NO guarda nada.
# Es como darle "guardar" despues de editar un archivo.
#
# conn.commit()     ← "guardalo de verdad"
# conn.rollback()   ← "deshaz todo, hubo un error"


# ── PREGUNTA: "Que hace rollback?" ───────────────────────────
# conn.rollback() DESHACE todo lo que se hizo desde el ultimo commit.
# Se usa dentro de un except (cuando algo falla).
# Es como Ctrl+Z para la base de datos.
#
# try:
#     cursor.executemany(query, data)   ← intenta meter los datos
#     conn.commit()                      ← si funciono, confirma
# except:
#     conn.rollback()                    ← si fallo, deshaz todo
#     raise                              ← y avisa que fallo


# ── PREGUNTA: "Que hace raise?" ──────────────────────────────
# raise RELANZA el error despues del rollback.
# Sin raise, el pipeline seguiria corriendo como si nada pasara
# y tu nunca te enterarias de que los datos no se guardaron.
#
# Es como: "primero apago el incendio (rollback),
# y DESPUES grito que hubo fuego (raise)."


# ── PREGUNTA: "Por que no cargaron a MySQL?" ─────────────────
# RESPUESTA:
# "Para 363 filas CSV era suficiente. Pero entendemos el proceso:
# CREATE TABLE dinamico recorriendo las columnas del DataFrame,
# executemany con placeholders %s, commit para confirmar
# y rollback si falla. Como vimos ayer en clase."


# ── PREGUNTA: "Por que crear la tabla desde codigo y no manual?" ──
# RESPUESTA:
# "Porque si manana el negocio agrega mas KPIs, la tabla manual se rompe.
# Desde codigo, el CREATE TABLE lee las columnas del DataFrame
# dinamicamente. No importa si son 16 o 25 columnas."
#
# El profe INSISTIO mucho en esto ayer. Es la respuesta que mas le importa.


# ── PREGUNTA: "Que son los placeholders %s?" ─────────────────
# Son HUECOS en el INSERT que se llenan con variables.
# INSERT INTO tabla (col1, col2) VALUES (%s, %s)
#
# Es mejor que poner valores fijos porque:
# 1. Es dinamico (funciona con cualquier dato)
# 2. Es seguro (previene SQL injection)
# 3. Es la mejor practica segun el profe


# ── PREGUNTA: "Que pasa con NaN cuando cargas a MySQL?" ──────
# Pandas usa NaN para valores vacios.
# MySQL NO entiende NaN. MySQL entiende NULL.
# Entonces hay que convertir: NaN → None (Python) → NULL (MySQL)
#
# data = [
#     tuple(None if pd.isna(valor) else valor for valor in fila)
#     for fila in df.itertuples(index=False)
# ]
# Eso es exactamente lo que el profe mostro ayer en la linea 64-67.


# ── PREGUNTA: "Que tipos de datos maneja pandas vs MySQL?" ───
# pandas          MySQL
# ───────         ─────
# object     →    VARCHAR(255)
# int64      →    INT
# float64    →    FLOAT
# datetime64 →    DATETIME
# NaN        →    NULL (via None)
#
# Hay que hacer la conversion en el load.py con una funcion map_dtype.


# ── PREGUNTA: "Que es la master table y por que 363 filas?" ──
# Una fila por dia de 2025.
# 365 dias - 2 dias de enero sin GA4 (se activo el 23) = 363.
# 16 columnas con metricas de las 5 fuentes unidas por fecha.


# ── PREGUNTA: "Que harian diferente?" ────────────────────────
# 1) Conectar WhatsApp de Meta con un CRM para medir conversion real
# 2) Campanas especificas para Auto Tradicional (vale 3.3x mas)
# 3) Cargar a MySQL o BigQuery con CREATE TABLE dinamico
# 4) Automatizar la extraccion via APIs en vez de CSVs manuales
# 5) Exponer el pipeline como API con FastAPI (orquestacion)


# ── PREGUNTA: "Que es Streamlit?" ────────────────────────────
# Libreria de Python que convierte un script en una app web.
# El profe la recomendo en clase para PREVISUALIZACION.
# No es BI final (como PowerBI o Tableau).
# Es la herramienta del ingeniero de datos para verificar su trabajo.
# Se corre con: streamlit run app.py


# ── PREGUNTA: "Que es ETL + AI que menciono el profe?" ───────
# Hoy en dia se conectan LLMs (modelos de lenguaje) en la etapa
# de transformacion para limpiar datos mas rapido.
# PERO: depende de la calidad del modelo.
# Son probabilisticos, tienen sesgos, pueden empeorar el dataset.
# No hay que fiarse del todo.
