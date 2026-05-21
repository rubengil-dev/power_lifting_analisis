"""
Funciones de visualización: gráficos de distribución y análisis.
"""

# IMPORTS
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
from .config import GRAPHS, PLOT_THEME, PLOT_RCPARAMS


# CONFIG DE GRÁFICOS
sns.set_theme(**PLOT_THEME)
plt.rcParams.update(PLOT_RCPARAMS)
warnings.filterwarnings('ignore', category = FutureWarning)

# GRÁFICOS DE EXPLORACIÓN: Simplemente muestran la distribución de la variable indicada

## DISTRIBUCIÓN EDAD
def plot_edad(df: pd.DataFrame):
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
def plot_peso(df: pd.DataFrame):
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
def plot_equipamiento(df: pd.DataFrame):
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
def plot_evento(df: pd.DataFrame):
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

## FUNCIÓN EXPLORACIÓN [ITSELF]
def plot_full_explore(df: pd.DataFrame):
    """
    Ejecuta todas las visualizaciones de distribución del dataset para solo poner una función en el main.py.
    """
    plot_edad(df)
    plot_peso(df)
    plot_equipamiento(df)
    plot_evento(df)

# GRÁFICOS DE RESPUESTA A PREGUNTAS ~ CADA FUNCIÓN CREA LOS GRÁFICOS DE SU PREGUNTA

# PREGUNTA 1
def graficos1(df: pd.DataFrame):
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
def graficos2(bench_df: pd.DataFrame, squat_df: pd.DataFrame, deadlift_df: pd.DataFrame):
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

# PREGUNTA 3
def graficos3(fail_global: pd.DataFrame, fail_sex_df: pd.DataFrame, fail_equip_df: pd.DataFrame):
    fig, ax = plt.subplots(nrows = 1, ncols = 3, figsize=(24, 6))

    ## SET DE NOMBRES
    ax[0].set_title("TASA DE ERROR POR EJERCICIO")
    ax[0].set_xlabel("EJERCICIO")
    ax[0].set_ylabel("TASA DE ERROR")

    ax[1].set_title("TASA DE ERROR POR EJERCICIO POR SEXO")
    ax[1].set_xlabel("EJERCICIO")
    ax[1].set_ylabel("TASA DE ERROR ")

    ax[2].set_title("TASA DE ERROR POR EJERCICIO POR EQUIPAMIENTO")
    ax[2].set_xlabel("EJERCICIO")
    ax[2].set_ylabel("TASA DE ERROR")

    # EJE AX[0] ~ PLOT GENERAL
    sns.barplot(
        data = fail_global,
        x = 'Levantamiento',
        y = 'FailRate',
        orient = 'v',
        errorbar = None,
        ax = ax[0]    
        )
    
    # TAGS
    ax[0].bar_label(ax[0].containers[0], fmt = '%.1f%%')

    # EJE AX[1] ~ PLOT POR SEXO
    sns.barplot(
        data = fail_sex_df,
        x = 'Levantamiento',
        y = 'FailRate',
        hue = 'Sex',
        palette = {'F': 'pink', 'M': 'blue'},
        errorbar = None,
        ax = ax[1]
        )

    # TAGS
    for container in ax[1].containers:
        ax[1].bar_label(container, fmt='%.1f%%')

    # LEYENDA
    sns.move_legend(ax[1], "upper right")

    # EJE AX[1] ~ PLOT POR SEXO
    sns.barplot(
        data = fail_equip_df,
        x = 'Levantamiento',
        y = 'FailRate',
        hue = 'Equipment',
        errorbar = None,
        ax = ax[2]
        )

    # TAGS
    for container in ax[2].containers:
        ax[2].bar_label(container, fmt='%.1f%%')

    # LEYENDA
    sns.move_legend(ax[2], "lower right")

    # SET DE OUTPUT
    plt.tight_layout()
    plt.savefig(GRAPHS / "pregunta3.png", bbox_inches = 'tight')
    plt.close(fig)

# PREGUNTA 4

## SUBGRÁFICO 1 ~ RENDIMIENTO POR EJERCICIO POR MODALIDAD
def plot_rendimiento_modalidad(bench_only_df: pd.DataFrame, squat_only_df: pd.DataFrame, deadlift_only_df: pd.DataFrame):
    fig, ax = plt.subplots(nrows = 1, ncols = 3, figsize = (18, 6))
    
    ## SET DE NOMBRES
    ax[0].set_title("RENDIMIENTO EN BANCA")
    ax[0].set_xlabel("MODALIDADES")
    ax[0].set_ylabel("RENDIMIENTO")
    
    ax[1].set_title("RENDIMIENTO EN SENTADILLA")
    ax[1].set_xlabel("MODALIDADES")
    ax[1].set_ylabel("RENDIMIENTO")

    ax[2].set_title("RENDIMIENTO EN PESO MUERTO")
    ax[2].set_xlabel("MODALIDADES")
    ax[2].set_ylabel("RENDIMIENTO")

    # EJE AX[0] ~ BANCA
    sns.barplot(
        data = bench_only_df,
        x = 'Event',
        y = 'Dot_Bench',
        orient = 'v',
        errorbar = None,
        ax = ax[0]    
    )

    # TAGS
    ax[0].bar_label(ax[0].containers[0], fmt = '%.2f')

    # EJE AX[0] ~ SENTADILLA
    sns.barplot(
        data = squat_only_df,
        x = 'Event',
        y = 'Dot_Squat',
        orient = 'v',
        errorbar = None,
        ax = ax[1]
    )

    # TAGS
    ax[1].bar_label(ax[1].containers[0], fmt = '%.2f')

    # EJE AX[0] ~ PESO MUERTO
    sns.barplot(
        data = deadlift_only_df,
        x = 'Event',
        y = 'Dot_Deadlift',
        orient = 'v',
        errorbar = None,
        ax = ax[2]
    )

    # TAGS
    ax[2].bar_label(ax[2].containers[0], fmt = '%.2f')

    # SET DE OUTPUT
    plt.tight_layout()
    plt.savefig(GRAPHS / "rendimiento_modalidad4.png", bbox_inches = 'tight')
    plt.close(fig)

## SUBGRÁFICO 2 ~ FAIL RATE
def plot_fail_rate4(df4b: pd.DataFrame):

    fig, ax = plt.subplots(figsize = (24, 6))

    ## SET DE NOMBRES
    ax.set_title("TASA DE ERROR EN 3ER INTENTO POR MODALIDAD")
    ax.set_xlabel("LEVANTAMIENTO")
    ax.set_ylabel("TASA DE ERROR ")

    # PLOT
    sns.barplot(
        data = df4b,
        x = 'Levantamiento',
        y = 'FailRate',
        orient = 'v',
        hue = 'Event',
        errorbar = None,
        ax = ax
        )

    # TAGS
    for container in ax.containers:
        ax.bar_label(container, fmt='%.1f%%')

    # SET DE OUTPUT
    plt.tight_layout()
    plt.savefig(GRAPHS / "fail_rate4.png", bbox_inches = 'tight')
    plt.close(fig)

## GRÁFICO 4 ITSELF
def graficos4(bench_only_df: pd.DataFrame, squat_only_df: pd.DataFrame, deadlift_only_df: pd.DataFrame, df4b: pd.DataFrame):
    plot_rendimiento_modalidad(bench_only_df, squat_only_df, deadlift_only_df)
    plot_fail_rate4(df4b)

# PREGUNTA 5
def graficos5(df: pd.DataFrame):
    fig, ax = plt.subplots(nrows = 1, ncols = 2, figsize = (18, 6))

    # SET DE NOMBRES
    ax[0].set_title("TASA DE ÉXITO DEL 4º INTENTO")
    ax[0].set_xlabel("EJERCICIO")
    ax[0].set_ylabel("TASA DE ÉXITO")

    ax[1].set_title("TASA DE ÉXITO DEL 4º INTENTO POR SEXO")
    ax[1].set_xlabel("EJERCICIO")
    ax[1].set_ylabel("TASA DE ÉXITO")

    # EJE AX[0] ~ PLOT GENERAL
    sns.barplot(
        data = df,
        x = 'Levantamiento',
        y = 'SuccessRate',
        orient = 'v',
        errorbar = None,
        ax = ax[0]    
        )

    # TAGS
    ax[0].bar_label(ax[0].containers[0], fmt = '%.1f%%')

    # EJE AX[1] ~ PLOT POR SEXO
    sns.barplot(
        data = df,
        x = 'Levantamiento',
        y = 'SuccessRate',
        orient = 'v',
        hue = 'Sex',
        errorbar = None,
        ax = ax[1]    
        )

    # TAGS
    for container in ax[1].containers:
        ax[1].bar_label(container, fmt='%.1f%%')

    # SET DE OUTPUT
    plt.tight_layout()
    plt.savefig(GRAPHS / "pregunta5.png", bbox_inches = 'tight')
    plt.close(fig)