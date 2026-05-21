"""
Modularización de la respuesta a las 5 preguntas del proyecto. De esta manera es más fácil gestionar el segundo filtrado del DF y permite que sólo corras las preguntas que te interesen.
"""

# IMPORTS
import pandas as pd
import pingouin as pg
from .viz import graficos1, graficos2, graficos3, graficos4, graficos5
from .features import pseudo_dots
from .utils import assert_nulls

# PREGUNTA 1
def pregunta1(df: pd.DataFrame):
    """Incluye toda la lógica para responder a la primera pregunta."""
    
    # LIMPIEZA CONCRETA
    df1 = df.dropna(subset = ['Age', 'Dots'])
    df1 = df1[(df1['Age'] >= 14) & (df1['Age'] <= 80)]
    df1['Age'] = df1['Age'].round()
    
    # ASSERTS
    assert_nulls(df1, 'Age', 'Dots')
    
    # PLOT
    graficos1(df1)

# PREGUNTA 2

## PREPARACIÓN DEL DF PARA EL ANÁLISIS ESTADÍSTICO
def prepare_df2(df: pd.DataFrame, lift: str):
    """Limpia, crea índice y pasa el df a formato largo."""

    # LIMPIEZA CONCRETA
    cols = [f'{lift}1Kg', f'{lift}2Kg', f'{lift}3Kg']
    df2 = df.dropna(subset = cols).copy()

    # INDICE ROBUSTO PARA ANOVA
    df2 = df2.reset_index(drop=True)
    df2['Idx'] = df2.index

    # DF ANCHO -> DF LARGO
    df2 = df2.melt(
        id_vars=['Name', 'Sex', 'Idx'],
        value_vars = cols,
        var_name = 'Intento',
        value_name = 'Peso'
    )

    return df2

## ANÁLISIS ESTADÍSTICO: ANOVA + POST-HOC
def analisis(df: pd.DataFrame):

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


## PREGUNTA 2 [ITSELF]
def pregunta2(df: pd.DataFrame):
    """Incluye toda la lógica para responder a la segunda pregunta."""

    # PREPARACIÓN
    bench_df = prepare_df2(df, 'Bench')
    squat_df = prepare_df2(df, 'Squat')
    deadlift_df = prepare_df2(df, 'Deadlift')

    # ASSERTS
    assert_nulls(bench_df, 'Peso', 'Intento')
    assert_nulls(squat_df, 'Peso', 'Intento')
    assert_nulls(deadlift_df, 'Peso', 'Intento')

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

    # PLOT
    graficos2(bench_df, squat_df, deadlift_df)

# PREGUNTA 3

## PREPARACIÓN DEL DF
def prepare_df3(df: pd.DataFrame):
    """Pasa el df a formato largo y luego limpia."""

    # DF ANCHO -> DF LARGO
    df3 = df.melt(
        id_vars = ['Name', 'Sex', 'Equipment'],
        value_vars = ['Bench3bool', 'Squat3bool', 'Deadlift3bool'],
        var_name = 'Levantamiento',
        value_name = 'Exito'
    )

    # LIMPIEZA CONCRETA
    return df3.dropna(subset = ['Exito'])

## NORMALIZAR FALLOS POR LEVANTAMIENTOS TOTALES
def fail_rate3(df: pd.DataFrame):
    """Calcula en 2 df diferentes el %Fallos sobre los levantamientos totales."""

    # GLOBAL
    fail_global = df.groupby('Levantamiento')['Exito'].apply(lambda x: (x == False).mean() * 100).reset_index(name = 'FailRate')
    
    # POR SEXO
    fail_sex_df = df.groupby(['Levantamiento', 'Sex'])['Exito'].apply(lambda x: (x == False).mean() * 100).reset_index(name = 'FailRate')

    # POR EQUIPO
    fail_equip_df = df.groupby(['Levantamiento', 'Equipment'])['Exito'].apply(lambda x: (x == False).mean() * 100).reset_index(name = 'FailRate')

    return fail_global, fail_sex_df, fail_equip_df

## PREGUNTA 3 [ITSELF]
def pregunta3(df: pd.DataFrame):
    """Incluye toda la lógica para responder a la tercera pregunta."""

    # LIMPIEZA CONCRETA
    df3 = prepare_df3(df)

    # ASSERTS
    assert_nulls(df3, 'Exito', 'Levantamiento')

    # FAIL RATE
    fail_global, fail_sex_df, fail_equip_df = fail_rate3(df3)

    # PLOT
    graficos3(fail_global, fail_sex_df, fail_equip_df)

# PREGUNTA 4

## PREPARACIÓN DEL DF
def prepare_df4(df: pd.DataFrame):
    """Divide el dataset por modalidad."""

    bench_only_df = df[~df['Event'].isin(['D', 'S', 'SD'])].dropna(subset = ['Best3BenchKg']).copy()
    squat_only_df = df[~df['Event'].isin(['D', 'B', 'BD'])].dropna(subset = ['Best3SquatKg']).copy()
    deadlift_only_df = df[~df['Event'].isin(['B', 'S', 'SB'])].dropna(subset = ['Best3DeadliftKg']).copy()

    return bench_only_df, squat_only_df, deadlift_only_df

## NORMALIZAR FALLOS POR LEVANTAMIENTOS TOTALES
def fail_rate4(df: pd.DataFrame):
    """Calcula el %Fallos por tipo de evento (SBD) sobre los levantamientos totales."""

    df4b = df.melt(
        id_vars = ['Name', 'Event'],
        value_vars = ['Bench3bool', 'Squat3bool', 'Deadlift3bool'],
        var_name = 'Levantamiento',
        value_name = 'Exito'
        )

    df4b = df4b.groupby(['Levantamiento', 'Event'])['Exito'].apply(lambda x: (x == False).sum() / x.dropna().count() * 100 if x.dropna().count() > 0 else np.nan).reset_index(name = 'FailRate')
    
    return df4b[df4b['FailRate'] > 0]

## PREGUNTA 4 [ITSELF]
def pregunta4(df: pd.DataFrame):
    """Incluye toda la lógica para responder a la cuarta pregunta."""

    # LIMPIEZA CONCRETA
    df4a = df.dropna(subset=['Event']).copy()

    # NUEVAS COLUMNAS
    df4a = pseudo_dots(df4a)

    # ASSERT
    assert_nulls(df4a, 'Event', 'Dot_Bench', 'Dot_Squat', 'Dot_Deadlift')

    # SPLIT POR MODALIDAD
    bench_only_df, squat_only_df, deadlift_only_df = prepare_df4(df4a)

    # FAIL RATE
    df4b = fail_rate4(df4a)

    # PLOT
    graficos4(bench_only_df, squat_only_df, deadlift_only_df, df4b)

# PREGUNTA 5

## PREPARACIÓN DEL DF
def prepare_df5(df: pd.DataFrame):
    """Pasa el df a formato largo para analizar éxito del 4º intento."""

    df5 = df.melt(
        id_vars=['Sex'],
        value_vars=['Bench4bool', 'Squat4bool', 'Deadlift4bool'],
        var_name='Levantamiento',
        value_name='Exito'
    )

    return df5.dropna(subset = ['Exito'])

## NORMALIZAR FALLOS POR LEVANTAMIENTOS TOTALES
def fail_rate5(df: pd.DataFrame):
    """Calcula % de éxito por levantamiento y sexo."""

    df5 = df.groupby(['Levantamiento', 'Sex'])['Exito'].apply(lambda x: (x == True).sum() / x.dropna().count() * 100).reset_index(name = 'SuccessRate')
    
    return df5

## PREGUNTA 5 [ITSELF]
def pregunta5(df: pd.DataFrame):
    """Incluye toda la lógica para responder a la quinta pregunta."""

    # LIMPIEZA CONCRETA
    df5 = prepare_df5(df)

    # ASSERT
    assert_nulls(df5, 'Exito', 'Levantamiento')

    # FAIL RATE
    df5 = fail_rate5(df5)

    # PLOT
    graficos5(df5)