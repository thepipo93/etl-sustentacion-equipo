# ETL Entrega Final — Guia del Equipo

## Equipo
Christian Trujillo | Alexandra Libreros | Juan Sebastian Hoyos | Koraima Torres

## Links importantes
- **Repo del proyecto:** [github.com/AlexaLibreros15/Proyecto_Final_ETL](https://github.com/AlexaLibreros15/Proyecto_Final_ETL)
- **Dashboard en vivo:** [thepipo93.github.io/etl-dashboard-ipalmera](https://thepipo93.github.io/etl-dashboard-ipalmera)

---

## Que espera el profe

### Viernes 27 — Revision tecnica en vivo
- Cada equipo proyecta su pantalla y muestra el pipeline corriendo
- El profe revisa el codigo, la estructura del repo, hace preguntas a cualquiera
- Es 100% tecnico — se habla de codigo

### Lunes 30 — Video de 15 minutos
- Estilo pitch / storytelling: problema → solucion → hallazgos
- CERO codigo en el video
- TODOS aparecemos y hablamos
- Se sube al Drive compartido

### La rubrica evalua 5 cosas:
1. Identificacion del problema
2. Extraccion de datos
3. Transformacion (limpieza, KPIs)
4. Carga (destino, reporte de calidad)
5. Presentacion final (storytelling)

---

## Que tenemos construido

### El Pipeline (4 archivos en src/)

| Archivo | Que hace |
|---|---|
| **extract.py** | Lee 6 CSVs de 5 fuentes con `pd.read_csv()` |
| **transform.py** | Limpia fechas, elimina duplicados y nulos, convierte QTZ→USD, calcula KPIs, merge por fecha |
| **load.py** | Guarda master_table.csv + genera reporte de calidad automatico |
| **pipeline.py** | Llama a los 3 en orden. Tiempo total: 0.2 segundos |

### Las 5 fuentes de datos

| Fuente | Filas | Que contiene |
|---|---|---|
| Google Ads | 1,219 | Inversion diaria, clics, conversiones por campana |
| Meta Ads | 26 | Inversion mensual, alcance, tipo de resultado |
| Google Analytics 4 | 7,446 | Sesiones diarias, usuarios, fuente de trafico (via BigQuery) |
| Search Console | 335 + 996 | Clics organicos diarios + terminos de busqueda |
| Ventas | 1,011 | Cada poliza vendida: producto, fecha, monto en Quetzales |

### Resultado: Master Table
- **363 filas** (una por dia del 2025) x **16 columnas**
- 0 nulos, 0 duplicados en todas las fuentes
- Guardada en `data/processed/master_table.csv`

---

## Los numeros que hay que saber

| KPI | Valor |
|---|---|
| Inversion total | $52,906 USD (Google Ads 81%, Meta 19%) |
| Revenue total | $187,413 USD |
| ROAS | 3.54x (por cada $1 invertido volvieron $3.54) |
| Polizas vendidas | 1,011 |
| Costo por poliza | $52 |
| Valor promedio poliza | $185 |

---

## Los 6 hallazgos del EDA

### 1. Performance Max es el formato mas eficiente
- 15% del presupuesto Google → 4,825 conversiones a $1.36 c/u
- Display gasto similar → 57 conversiones a $34.63 c/u
- **Display cuesta 25x mas por conversion**

### 2. Meta WhatsApp no tiene trazabilidad
- $4,262 invertidos → 22 mensajes WhatsApp a $193 c/u
- No hay forma de saber si se convirtieron en polizas (no hay CRM conectado)
- Meta Trafico SI funciono: 186,688 visitas a $0.02/clic

### 3. El organico crecio en el segundo semestre
- Sep y Oct = menor inversion pero mayor trafico web
- Segundo semestre = 72% de todas las visitas del ano
- El canal organico compenso la reduccion de pauta

### 4. Dos productos con valores muy distintos
- Auto por Kilometro: 967 polizas, $168 promedio (87% del revenue)
- Auto Tradicional: 44 polizas, $560 promedio (13% del revenue)
- Una poliza Tradicional = 3.3 polizas KM en valor
- No hay campanas especificas para Auto Tradicional

### 5. Las ventas no siguen la inversion
- Marzo: $3,809 invertidos → 107 polizas (mejor mes)
- Abril: $6,286 invertidos → 75 polizas (peor relacion)
- Ventas estables entre 69 y 107/mes todo el ano

### 6. Busquedas organicas
- 58,978 impresiones en Google
- 2,668 clics organicos (CTR 4.5%)
- Posicion promedio 4.2 (primer resultado primera pagina)
- Marzo = mas clics organicos = mas polizas

---

## Preguntas que el profe puede hacer

### Sobre el pipeline

**P: Que hace extract.py?**
> Lee los 6 CSVs crudos de data/raw/ con pd.read_csv() y los devuelve como DataFrames.

**P: Que hace transform.py?**
> Estandariza fechas (cada fuente tenia formato diferente), elimina duplicados (0), nulos (0), calcula KPIs (CPM, CPC, CPA), y une las 5 fuentes por fecha con merge. Resultado: Master Table 363x16.

**P: Que es un merge?**
> Unir dos tablas por una columna en comun. En nuestro caso "fecha". how='outer' para incluir todos los dias aunque una fuente no tenga datos.

**P: Por que CSV y no base de datos?**
> Para 363 filas CSV es suficiente. Para produccion: MySQL con CREATE TABLE dinamico, cursor.executemany(), commit/rollback.

**P: Que es la master table y por que 363?**
> Una fila por dia de 2025 (365 - 2 dias enero sin GA4 = 363). 16 columnas con metricas de las 5 fuentes.

### Sobre los datos

**P: Que es ROAS?**
> Revenue / Inversion = $187,413 / $52,906 = 3.54x. Por cada dolar invertido volvieron $3.54.

**P: Que pasa con NaN?**
> En transform: fillna(0). Si fuera MySQL: NaN → None → NULL (MySQL no entiende NaN).

**P: Diciembre por que tiene 143K sesiones?**
> Alta inversion ($6,413) + crecimiento organico del segundo semestre + estacionalidad fin de ano.

**P: Que harian diferente?**
> 1) Conectar WhatsApp con CRM. 2) Campanas para Auto Tradicional. 3) Cargar a MySQL/BigQuery. 4) Automatizar extraccion via APIs. 5) Exponer como API con FastAPI.

### Sobre lo que vimos en la ultima clase

**P: Que hace el cursor?**
> Puntero que ejecuta comandos SQL. cursor.execute() manda el comando, cursor.executemany() mete muchas filas de un golpe.

**P: Que hace commit?**
> Confirma la transaccion. Sin commit no se guarda nada.

**P: Que hace rollback?**
> Deshace todo si algo falla. Es el Ctrl+Z de la base de datos.

**P: Que son los placeholders %s?**
> Huecos en el INSERT que se llenan con variables. Mejor practica que valores fijos porque es dinamico y seguro.

**P: Por que crear la tabla desde codigo?**
> Porque si el negocio agrega KPIs, la tabla manual se rompe. Desde codigo el CREATE TABLE lee las columnas del DataFrame dinamicamente.

**P: Que es Streamlit?**
> Libreria Python que convierte un script en app web. El profe la recomendo para previsualizacion. No es BI final.

---

## Para correrlo en tu PC

```bash
git clone https://github.com/AlexaLibreros15/Proyecto_Final_ETL.git
cd Proyecto_Final_ETL
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
cd src
python pipeline.py             # corre el pipeline completo
```

Para Streamlit:
```bash
cd ..
streamlit run app.py           # abre dashboard en localhost:8501
```

---

## Secciones para dividir (viernes)

| Seccion | Que hablar |
|---|---|
| **Extraccion** | De donde vienen los datos, cuantas filas, como se leen |
| **Transformacion** | Que limpieza se hizo, merge, conversion QTZ→USD |
| **Carga + Calidad** | Como se guarda, reporte de calidad, tiempo |
| **EDA + Dashboard** | Los 6 hallazgos, que funciono, que no |

Todos leemos TODO para poder responder cualquier pregunta.
