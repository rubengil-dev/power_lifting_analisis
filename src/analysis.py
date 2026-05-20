"""
Modularización de la respuesta a las 5 preguntas del proyecto. De esta manera es más fácil gestionar el segundo filtrado del DF y permite que sólo corras las preguntas que te interesen.
"""

# IMPORTS
import pandas as pd
import pingouin as pg
from src.viz import graficos1, graficos2, graficos3, graficos4, graficos5

# PREGUNTA 1
def pregunta1(df: pd.DataFrame):
    """Incluye toda la lógica para responder a la primera pregunta."""

    # LIMPIEZA CONCRETA
    df1 = df.dropna(subset = ['Age', 'Dots'])
    df1 = df1[(df1['Age'] >= 14) & (df1['Age'] <= 80)]
    df1['Age'] = df1['Age'].round().copy()

    # PLOT
    graficos1(df1)

# PREGUTNA 2

## PREPARACIÓN DEL DF PARA EL ANÁLISIS ESTADÍSTICO
def prepare_df2(df: pd.DataFrame, lift: str):
    """Limpia, crea índice y pasa el df a formato largo."""

    # LIMPIEZA CONCRETA
    cols = [f'{lift}1Kg', f'{lift}2Kg', f'{lift}3Kg']
    df2 = df.dropna(subset = cols).copy()

    # INDICE ROBUSTO PARA ANOVA
    df2 = df2.reset_index(drop=True)
    df2['Idx'] = df2.index

    # TRANSFORMACIÓN PARA ANOVA
    df2 = df2.melt(
        id_vars=['Name', 'Sex', 'Idx'],
        value_vars = cols,
        var_name = 'Intento',
        value_name = 'Peso'
    )

    return df2

## ANÁLISIS ESTADÍSTICO: ANOVA + POST-HOC
def analisis(df):

    # ANOVA
    anova = pg.rm_anova(
        data = df,
        dv = 'Peso',
        within = 'Intento',
        subject = 'Idx',
        effsize = 'n2'
    )

    # POST-HOC
    posthoc = pg.pairwise_tests(
        data = df,
        dv = 'Peso',
        within = 'Intento',
        subject = 'Idx',
        alpha = 0.05,
        alternative = 'two-sided',
        padjust = 'bonf',
        effsize = 'cohen',
        return_desc = True
    )

    return anova, posthoc


## PREGUTNA 2 [ITSELF]
def pregunta2(df: pd.DataFrame):
    """Incluye toda la lógica para responder a la segunda pregunta."""

    # PREPARACIÓN
    bench_df = prepare_df2(df, 'Bench')
    squat_df = prepare_df2(df, 'Squat')
    deadlift_df = prepare_df2(df, 'Deadlift')

    # ANÁLISIS
    bench_anova, bench_posthoc = analisis(bench_df)
    squat_anova, squat_posthoc = analisis(squat_df)
    deadlift_anova, deadlift_posthoc = analisis(deadlift_df)

    # OUTPUT
    print("- - - - - ANÁLISIS BANCA - - - - - ")
    print(bench_anova)
    print(bench_posthoc)

    print("- - - - - ANÁLISIS SENTADILLA - - - - - ")
    print(squat_anova)
    print(squat_posthoc)

    print("- - - - - ANÁLISIS PESO MUERTO - - - - - ")
    print(deadlift_anova)
    print(deadlift_posthoc)

    graficos2(bench_df, squat_df, deadlift_df)

def pregunta3(df: pd.DataFrame):
    """Incluye toda la lógica para responder a la tercera pregunta."""

    return

def pregunta4(df: pd.DataFrame):
    """Incluye toda la lógica para responder a la cuarta pregunta."""

    return

def pregunta5(df: pd.DataFrame):
    """Incluye toda la lógica para responder a la quinta pregunta."""

    return

