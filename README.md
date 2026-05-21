## Plantilla de README

### 1) Objetivo
Analizar el rendimiento de atletas de powerlifting en competiciones oficiales y bajo control antidopaje, respondiendo a 5 preguntas concretas sobre edad, progresión, fallos y especialización con la intención de obtener insights claros para apoyar la estrategia de los atletas durante la competición.

### 2) Dataset
Para el proyecto utilicé el CSV open source de **Open PowerLifing**. Originalmente tiene ~ 3.9M filas y 42 columnas. Todas y cada una de las variables del dataset están definidas en `OPL_guide.txt` que va adjunto al proyecto (es el README.md de su proyecto). Lo descargué directamente en `data` con el nombre de `OPL_dataset.csv`. Lo podéis descargar en: [Open Powerlifting](https://openpowerlifting.gitlab.io/opl-csv/bulk-csv.html).

Es el que se llama `openpowerlifting-latest.zip` con un tamaño de 158Mb y 3.925.888 rows (en el momento que yo lo descargué [05/2026]). 

### 3) Preguntas
Las preguntas que quise responder fueron:

1. ¿A qué edad alcanzan el pico de rendimiento los atletas? ¿Difiere entre hombres y mujeres?
2. ¿Cómo progresan los atletas dentro de una competición? ¿Suben de peso entre intentos 1 → 2 → 3 o tienden a repetir/bajar?
3. ¿En qué levantamiento (squat, bench, deadlift) se producen más fallos en el 3er intento?
4. ¿Los atletas que compiten en más eventos full lifting rinden más o menos que los que se especializan en un sólo tipo de levantamiento?
5. ¿Qué éxito tiene el 4º intento? ¿Realmente logran superarse?

### 4) Data issues & fixes
El principal problema del dataset es la gran cantidad de nulos que tiene en la mayoría de columnas y, que muchos de esos nulos son válidos. Si un atleta no ha hecho un levantamiento, la columna es nula. Para sortear este primer problema tome una decisión: Con las columnas disponibles, imputé el máximo de valores posibles de todas las columnas pertinentes, pero no rellené los datos artificialmente con medias o medianas para ser fiel a los datos originales. Tras esta limpieza inicial, para cada una de las preguntas el DF es pre-filtrado para quitar los NaNs pertinentes. De esta forma, me ahorraba perder gran cantidad de datos relevantes de una pregunta a otra, cosa que habría sido imposible limpiando a nivel general.

Otro gran problema del conjunto de datos es que los lanzamientos que intentan los atletas (es decir, existen), que han sido fallados, se apuntan como valores negativos. Estos valores son un problema porque desvirtuan la media y además, no aportan demasiada información más allá de que el levantamiento existe y que se ha fallado. Por eso, en el proceso de limpieza seguí el siguiente pipelane:

1. Cree unas columnas tipo `boolean` (para que gestionen NaN), donde registraba si el levantamiento había sido exitoso `True`, fallido `False`, o no se había realizado `NaN`. Lo hice solo para los 3 y 4 levantamiento de cada ejercicio, pues son los únicos que necesitaba para analizar.
2. Una vez creadas estas columnas (y no al revés), todos los valores de las columnas que registran levantamientos que eran 0 o negativas fueron transformadas a `NaN`. De esta manera al filtrar posteriormente para responder a las preguntas estos valores desaparecerían.

A su vez, en el dataset original había 4 métricas de rendimiento Dots, Wilks, Glossbrenner y Goodlift. Finalmente me quedé solo con Dots, la más actual, y traté de imputarla con las otras pero no pude porque cuando Dots era NaN, las otras también. Al final, para responder a la pregunta 4 creo una métrica nueva, muy sencilla, para evaluar el rendimiento estandarizadamente sin tener en cuenta si los atletas hicieron uno o varios ejercicios. Comprobé que correlacionaba adecuadamente con Dots (r > 0.85).

Por último, como en la mayoría de datasets '_sucios_', tuve que cambiar tipos, filtrar según mis intereses (competiciones oficiales y natty (no dopaje)), además de realizar las transformaciones pertinentes al dataframe para poder correr test como **ANOVA** o **POST-HOC** en la pregunta 2.

Todo el proceso de limpieza previa se puede apreciar en `src/cleaning.py` y la limpieza específica de cada pregunta en `src/analysis.py`. También puede apreciarse la exploración y limpieza en las secciones 3-6 del cuaderno en `notebooks/eda.ipynb`.

### 5) Pipeline

El pipelane se puede apreciar claramente en el `main.py`, pero básicamente fue el siguiente:

1. **Carga y pre-filtrado del df**: Antes si quiera de empezar la exploración, tras revisar `OPL_guide.txt`, reduje las dimensiones del df y filtré para quedarme solo con las columnas que usaría y datos de atletas en competiciones oficiales y anti-dopaje.
2. **Limpieza**: Consistió en eliminar duplicados absolutos, arreglar los tipos e imputar el máximo número de nulos posible (no eliminarlos).
3. *Feature* 1: Antes de terminar la limpieza tenía que crear las columnas booleanas o sino después sería imposible.
4. *Terminar* limpieza: Arreglé los negativos de las columnas de lanzamientos y eliminé las filas del sexto mixto dado su escaso número de datos (~100) y para facilitar el análisis.
5. *Asserts*: Comprobamos que toda la limpieza ha salido correctamente (negativos, columnas eliminadas y creadas...)
6. *Guardado* y exploración: La idea era guardar el dataset limpio y observar las 4 variables '_tag_' principales del dataset: Edad, Sexo, Tipo de evento (SBD) y Equipamiento permitido (sección 6 del `notebooks/eda.ipynb`).
7. *Análisis*: Este punto es el más largo, pues consta de 5 subpuntos donde, en cada uno, respondo a una de las preguntas y muestro sus gráficos (secciones 7 y 8 del `notebooks/eda.ipynb`).

### 6) Hallazgos

- El mejor momento para un atleta de powerlifting llega en torno a los 22 años y se mantiene hasta los 24, a partir de los cuales empieza a decaer cada vez de forma más acelerada.

- El press de banca es notablemente distinto al peso muerto y a la sentadilla, ya que es el único ejercicio donde se ve una clara mejora del rendimiento por especialización y es el único con una tasa de fallos al tercer intento mayor al 50%. Para sentadilla y peso muerto parece que la fuerza desarrollada en el resto de ejercicios es transferible y su tasa de fallo es mucho menor (~30%).
[Conclusión a tomar con precaución dada la asimetría de los datos].

- La tendencia de todos los atletas a superar su anterior levantamiento en el siguiente sugiere que el levantamiento más importante en la competición es el último. A su vez, el número de fallos en este último levantamiento es elevado, especialmente en banca. En conjunto, ambos datos pueden ayudar a diseñar una estrategia basada en arriesgar en el segundo levantamiento para ejercer presión sobre el resto de participantes.

- Es recomendable a todos los atletas realizar el cuarto levantamiento, ya que al estar libre de presión, tiene una tasa de éxito del ~ 80% (a falta de comprobar que no haya sesgo de publicación). Esto es enormemente importante de cara a la preparación de próximas competiciones.

- **Nota extra**: No se han apreciado diferencias por sexo en ninguna de las características estudiadas salvo, la obvia diferencia en cargas absolutas, que desaparece tras normalizar por peso.

De cara a un análisis futuro sería conveniente:

- Diseñar un modelo que prediga cuál será el máximo peso que el atleta podrá levantar sin fallar en su siguiente intento, ayudando así, nuevamente a la planificación de la competición.

- Sería interesante incorporar datos biológicos como horas de sueño, dieta y descanso previos a las competiciones para hacer un análisis más robusto.

- Podría ser interesante repetir este estudio manteniendo sólo la categoría SBD (full lifting), ya que parece ser la predominante. De esta manera, los resultados serían aún más transferibles.

### 7) Estructura del proyecto

```
project/
├── .venv/                          # ENTORNO VIRTUAL
├── data/                           # DATASETS Y GRÁFICOS
│   ├── output_graphs/                  # GRÁFICOS
│   ├── clean_dataset.csv               # CLEAN
│   └── OPL_dataset.csv                 # RAW
├── notebooks/
│   └── eda.ipynb                   # CUADERNO FULL PIPELANE
├── src/                            # MODULARIZACIÓN DEL PIPELANE
│   ├── __init__.py
│   ├── analysis.py                 # FUNCIONES DE RESPUESTA A LAS 5 PREGUNTAS
│   ├── cleaning.py                 # FUNCIONES DE LIMPIEZA
│   ├── config.py                   # CONFIGURACIÓN
│   ├── features.py                 # NUEVAS COLUMNAS
│   ├── io.py                       # SET UP DE CARGA Y DESCARGA DEL DF
│   ├── utils.py                    # FUNCIONES AUXILIARES DEL RESTO DE MÓDULOS + ASSERTS
│   └── viz.py                      # GRÁFICOS
├── .gitignore
├── OPL_guide.txt                   # GUIA DE OPL PARA MAYOR COMPRENSIÓN DEL DF
├── main.py                         # ARCHIVO ORQUESTA DEL PROYECTO
├── README.md                       # LA GUÍA QUE ESTAS LEYENDO
└── requirements.txt                # LOS REQUIREMENTS DEL .venv
```

### 8) Cómo ejecutar

**1. PASO 1 ~ DESCARGAR EL DATASET**

  I. Ir a [text](https://openpowerlifting.gitlab.io/opl-csv/bulk-csv.html) y descargar el FULL DATASET.
 II. Ponerlo en la carpeta `data`.
III. **[Opción A ~ Recomendada]** Cambiar el nombe a `OPL_dataset.csv` (copy-paste).
 IV. [Opción B] **Si decides no cambiar el nombre**, debes:
- En el archivo `main.py`, cambia la línea 23:
```python
# LINEA ACTUAL
df = load(DATA / "OPL_dataset.csv")

# TU LINEA
df = load(DATA / "tu_nombre_archivo.csv")
```

- En el notebooks/eda.ipynb cambia la sección de CARGA:
```python
# LINEA ACTUAL
        opl_df = pd.read_csv('../data/OPL_dataset.csv', low_memory = False)

# TU LINEA
        opl_df = pd.read_csv('../data/tu_nombre_archivo.csv', low_memory = False)
```

**2. PASO 2 ~ CREAR, ACTIVAR, Y PREPARAR EL ENTORNO**

El siguiente bloque de código debe ser escrito POR PASOS (línas de 1 en 1), en la terminal de tu ordenador.

**MAX/LINUX**
```bash
python -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt
```

**WINDOWS**
```powershell
python -m venv .venv

.venv\Scripts\activate

pip install -r requirements.txt
```
**3. PASO 3 ~ EJECUTAR EL PROYECTO**
```PowerShell
python main.py
```

PD1: También puedes ejecutar y ver el notebook para mayor claridad y explicaciones :)

PD2: Tarda un poquito porque las operaciones no están del todo optimizadas :)