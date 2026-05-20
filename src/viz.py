"""
Funciones de visualización: gráficos de distribución y análisis.
"""

# IMPORTS
import matplotlib.pyplot as plt
import seaborn as sns
from src.config import GRAPHS

# GRÁFICOS DE EXPLORACIÓN: Simplemente muestran la distribución de la variable indicada

## DISTRIBUCIÓN EDAD
def plot_edad(df):
    fig, ax = plt.subplots(nrows = 1, ncols = 2, figsize = (12, 6))

    # SET DE NOMBRES
    ax[0].set_title("HISTOGRAMA EDAD")
    ax[0].set_xlabel("EDAD[AÑOS]")
    ax[0].set_ylabel("FRECUENCIA")

    ax[1].set_title("BOXPLOT EDAD")
    ax[1].set_xlabel("SEXO")
    ax[1].set_ylabel("EDAD[AÑOS]")

    # EJE AX[0] ~ HISTOGRAMA
    sns.histplot(data = df, x = 'Age', binwidth = 3, kde = True, ax = ax[0])

    # EJE AX[1] ~ BOXPLOT
    sns.boxplot(data = df, x = 'Sex', y = 'Age', palette = {'F': 'pink', 'M': 'blue'}, ax = ax[1])

    # SET DE OUTPUT
    plt.tight_layout()
    plt.savefig(GRAPHS / "distribucion_edad.png", bbox_inches = 'tight')
    plt.close(fig)

## DISTRIBUCIÓN PESO
def plot_peso(df):
    fig, ax = plt.subplots(nrows = 1, ncols = 2, figsize = (12, 6))

    # SET DE NOMBRES
    ax[0].set_title("HISTOGRAMA PESO")
    ax[0].set_xlabel("PESO[KG]")
    ax[0].set_ylabel("FRECUENCIA")

    ax[1].set_title("BOXPLOT PESO")
    ax[1].set_xlabel("SEXO")
    ax[1].set_ylabel("PESO[KG]")

    # EJE AX[0] ~ HISTOGRAMA
    sns.histplot(data = df, x = 'BodyweightKg', binwidth = 5, kde = True, ax = ax[0])

    # EJE AX[1] ~ BOXPLOT
    sns.boxplot(data = df, x = 'Sex', y = 'BodyweightKg', palette = {'F': 'pink', 'M': 'blue'}, ax = ax[1])

    # SET DE OUTPUT
    plt.tight_layout()
    plt.savefig(GRAPHS / "distribucion_peso.png", bbox_inches = 'tight')
    plt.close(fig)

## DISTRIBUCIÓN EQUIPAMIENTO
def plot_equipamiento(df):
    fig, ax = plt.subplots(nrows = 1, ncols = 2, figsize = (12, 6))

    # SET DE NOMBRES
    ax[0].set_title("DISTRIBUCIÓN EQUIPAMIENTO")
    ax[0].set_xlabel("EQUIPAMIENTO")
    ax[0].set_ylabel("FRECUENCIA")

    ax[1].set_title("DISTRIBUCIÓN EQUIPAMIENTO POR SEXO")
    ax[1].set_xlabel("EQUIPAMIENTO")
    ax[1].set_ylabel("FRECUENCIA")

    # EJE AX[0] ~ RECUENTO
    sns.countplot(data = df, x = 'Equipment', ax = ax[0])

    # EJE AX[1] ~ RECUENTO POR SEXO
    sns.countplot(data = df, x = 'Equipment', hue = 'Sex', palette = {'F': 'pink', 'M': 'blue'}, ax = ax[1])

    # SET DE OUTPUT
    plt.tight_layout()
    plt.savefig(GRAPHS / "distribucion_equipamiento.png", bbox_inches = 'tight')
    plt.close(fig)

## DISTRIBUCIÓN EVENTO
def plot_evento(df):
    fig, ax = plt.subplots(nrows = 1, ncols = 2, figsize = (12, 6))

    # SET DE NOMBRES
    ax[0].set_title("DISTRIBUCIÓN EVENTO")
    ax[0].set_xlabel("EVENTO")
    ax[0].set_ylabel("FRECUENCIA")

    ax[1].set_title("DISTRIBUCIÓN EVENTO POR SEXO")
    ax[1].set_xlabel("EVENTO")
    ax[1].set_ylabel("FRECUENCIA")
    
    # EJE AX[0] ~ RECUENTO
    sns.countplot(data = df, x = 'Event', ax = ax[0])

    # EJE AX[1] ~ RECUENTO POR SEXO
    sns.countplot(data=df, x='Event', hue='Sex', palette={'F': 'pink', 'M': 'blue'}, ax=ax[1])

    # SET DE OUTPUT
    plt.tight_layout()
    plt.savefig(GRAPHS / "distribucion_evento.png", bbox_inches = 'tight')
    plt.close(fig)

## FUNCIÓN CONTENEDORA DE EXPLORACIÓN
def plot_full_explore(df):
    """
    Ejecuta todas las visualizaciones de distribución del dataset para solo poner una función en el main.py.
    """
    plot_edad(df)
    plot_peso(df)
    plot_equipamiento(df)
    plot_evento(df)

# GRÁFICOS DE RESPUESTA A PREGUNTAS ~ CADA FUNCIÓN CREA LOS GRÁFICOS DE SU PREGUNTA

# PREGUNTA 1
def graficos1(df):
    fig, ax = plt.subplots(nrows = 1, ncols = 2, figsize = (12, 6))

    # SET DE NOMBRES
    ax[0].set_title("Rendimiento según la EDAD y el SEXO")
    ax[0].set_xlabel("EDAD")
    ax[0].set_ylabel("RENDIMIENTO[DOTS]")

    ax[1].set_title("Rendimiento según la EDAD y el SEXO")
    ax[1].set_xlabel("EDAD")
    ax[1].set_ylabel("RENDIMIENTO[DOTS]")
    ax[1].set_xlim(16, 33)

    # EJE AX[0] ~ TENDENCIA RENDIMIENTO X EDAD
    sns.lineplot(
            data = df,
            x = 'Age',
            y = 'Dots',
            hue = 'Sex',
            palette = {
                'F': 'pink',
                'M': 'blue'
                },
            ax = ax[0]
            )

    # EJE AX[1] ~ ZOOM ENTRE 16 Y 33
    sns.lineplot(
            data = df,
            x = 'Age',
            y = 'Dots',
            hue = 'Sex',
            palette = {
                'F': 'pink',
                'M': 'blue'
                },
            ax = ax[1]
            )

    # TAGS DEL ZOOM
    for line in ax[1].lines:
        for x, y in zip(line.get_xdata(), line.get_ydata()):
            ax[1].annotate(f'{x:.0f}, {y: .0f}', (x, y), fontsize = 10)

    # SET DE OUTPUT
    plt.tight_layout()
    plt.savefig(GRAPHS / "pregunta1.png", bbox_inches = 'tight')
    plt.close(fig)


# PREGUNTA 2
def graficos2(bench_df, squat_df, deadlift_df):
    fig, ax = plt.subplots(nrows = 3, ncols = 2, figsize = (10, 10))

    # BENCH
    ## SET DE NOMBRES
    ax[0][0].set_title("PROGRESIÓN EN BANCA")
    ax[0][0].set_xlabel("INTENTO")
    ax[0][0].set_ylabel("PESO LEVANTADO [KG]")

    ax[0][1].set_title("PROGRESIÓN EN BANCA POR SEXO")
    ax[0][1].set_xlabel("INTENTO")
    ax[0][1].set_ylabel("PESO LEVANTADO [KG]")

    # EJE AX[0][0] ~ PROGRESIÓN BANCA
    sns.boxplot(data = bench_df, x = 'Intento', y = 'Peso', ax = ax[0][0])
    
    # EJE AX[0][1] ~ PROGRESIÓN BANCA POR SEXO
    sns.boxplot(data = bench_df, x = 'Intento', y = 'Peso', hue = 'Sex', palette={'F': 'pink', 'M': 'blue'}, ax=ax[0][1])

    # SENTADILLA
    ## SET DE NOMBRES
    ax[1][0].set_title("PROGRESIÓN EN SENTADILLA")
    ax[1][0].set_xlabel("INTENTO")
    ax[1][0].set_ylabel("PESO LEVANTADO [KG]")

    ax[1][1].set_title("PROGRESIÓN EN SENTADILLA POR SEXO")
    ax[1][1].set_xlabel("INTENTO")
    ax[1][1].set_ylabel("PESO LEVANTADO [KG]")

    # EJE AX[1][0] ~ PROGRESIÓN SENTADILLA
    sns.boxplot(data = squat_df, x = 'Intento', y = 'Peso', ax = ax[1][0])

    # EJE AX[1][1] ~ PROGRESIÓN SENTADILLA POR SEXO
    sns.boxplot(data = squat_df, x = 'Intento', y = 'Peso', hue = 'Sex', palette = {'F': 'pink', 'M': 'blue'}, ax=ax[1][1])

    # PESO MUERTO
    ## SET DE NOMBRES
    ax[2][0].set_title("PROGRESIÓN EN PESO MUERTO")
    ax[2][0].set_xlabel("INTENTO")
    ax[2][0].set_ylabel("PESO LEVANTADO [KG]")

    ax[2][1].set_title("PROGRESIÓN EN PESO MUERTO POR SEXO")
    ax[2][1].set_xlabel("INTENTO")
    ax[2][1].set_ylabel("PESO LEVANTADO [KG]")

    # EJE AX[2][0] ~ PROGRESIÓN PESO MUERTO
    sns.boxplot(data = deadlift_df, x = 'Intento', y = 'Peso', ax = ax[2][0])

    # EJE AX[2][1] ~ PROGRESIÓN PESO MUERTO POR SEXO
    sns.boxplot(data = deadlift_df, x = 'Intento', y = 'Peso', hue = 'Sex', palette = {'F': 'pink', 'M': 'blue'}, ax=ax[2][1])

    # SET DE OUTPUT
    plt.tight_layout()
    plt.savefig(GRAPHS / "pregunta2.png", bbox_inches = 'tight')
    plt.close(fig)
