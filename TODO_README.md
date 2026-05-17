## Plantilla de README

### 1) Objetivo
- Analizar y visualizar un dataset de demostración para entender el proceso de limpieza de datos, construcción de características y generación de visualizaciones.

### 2) Dataset
- Fuente: Archivo CSV de ejemplo (demo_dirty.csv)
- Nº filas/columnas: Variable (depende del archivo cargado)
- Variables clave: Columnas de datos numéricos y categóricos para análisis

### 3) Preguntas
- Q1: ¿Cómo se distribuyen los datos después de la limpieza?
- Q2: ¿Qué características nuevas se pueden derivar?

**Preguntas de negocio**

1. ¿A qué edad alcanzan el pico de rendimiento los atletas (medido con Dots) y difiere entre hombres y mujeres?
2. ¿Cómo progresan los atletas dentro de una competición? ¿Suben de peso entre intentos 1→2→3 o tienden a repetir/bajar?
3. ¿En qué levantamiento (squat, bench, deadlift) se producen más fallos en el 3er intento?
4. ¿Los atletas que compiten en más eventos full lifting rinden más o menos que los que se especializan en un sólo tipo de levantamiento?
5. ¿El 4º intento permite a los atletas superar su mejor marca de los 3 primeros? ¿Cuál es la tasa de éxito?

### 4) Data issues & fixes
- Valores faltantes → Limpieza y imputación en src/cleaning.py
- Datos inconsistentes → Normalización y corrección
- Formatos incorrectos → Conversión de tipos de datos

### 5) Pipeline
- raw → clean → features → viz → (export opcional a `data/processed/`)

### 6) Hallazgos
- Insight 1: Distribución de datos limpia (con referencia a gráfico generado)
- Insight 2: Características derivadas mejoran el análisis
- Insight 3: Visualizaciones revelan patrones clave

### 7) Estructura del proyecto
- `src/` contiene funciones reutilizables (`io`, `cleaning`, `features`, `viz`)
- `main.py` ejecuta el pipeline end-to-end

### 8) Cómo ejecutar
- `pip install -r requirements.txt`
- Ejecutar pipeline: `python main.py`
- (Opcional) Abrir y ejecutar: `notebooks/eda.ipynb`

## Estructura recomendada del proyecto

Regla: el notebook **explica** y **orquesta**. El código repetible va a `src/`.

Estructura sugerida:

```
project/
├── main.py
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
│   └── eda.ipynb
├── src/
│   ├── __init__.py
│   ├── io.py
│   ├── cleaning.py
│   ├── config.py
│   ├── features.py
│   ├── viz.py
│   └── utils.py
├── README.md
├── .gitignore
└── requirements.txt

```