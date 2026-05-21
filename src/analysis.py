"""
Modularization of the answers to the 5 project questions. This makes managing the second filtering of the DF easier and allows you to run only the questions you are interested in.
"""

# IMPORTS
import pandas as pd
import numpy as np
import pingouin as pg
from .viz import graphs1, graphs2, graphs3, graphs4, graficos5
from .features import pseudo_dots
from .utils import assert_nulls

# QUESTION 1


def question1(df: pd.DataFrame):
    """Includes all the logic to answer the first question."""

    # CONCRET CLEANING
    df1 = df.dropna(subset=['Age', 'Dots'])
    df1 = df1[(df1['Age'] >= 14) & (df1['Age'] <= 80)]
    df1['Age'] = df1['Age'].round()

    # ASSERTS
    assert_nulls(df1, 'Age', 'Dots')

    # PLOT
    graphs1(df1)

# QUESTION 2

# DF PREPARATION FOR STADISTIC ANALYSIS


def prepare_df2(df: pd.DataFrame, lift: str):
    """Clean, create the index, and melt the df into long format."""

    # CONCRET CLEANING
    cols = [f'{lift}1Kg', f'{lift}2Kg', f'{lift}3Kg']
    df2 = df.dropna(subset=cols).copy()

    # ROBUST INDEX FOR ANOVA
    df2 = df2.reset_index(drop=True)
    df2['Idx'] = df2.index

    # WIDE DF -> LONG DF
    df2 = df2.melt(
        id_vars=['Name', 'Sex', 'Idx'],
        value_vars=cols,
        var_name='Intento',
        value_name='Peso'
    )

    return df2

# STADISTIC ANALYSIS: ANOVA + POST-HOC


def analisis(df: pd.DataFrame):
    """Runs ANOVA + Post-HOC analysis for a melted dataframe."""

    # ANOVA
    anova = pg.rm_anova(
        data=df,
        dv='Peso',
        within='Intento',
        subject='Idx',
        effsize='n2'
    )

    # POST-HOC
    posthoc = pg.pairwise_tests(
        data=df,
        dv='Peso',
        within='Intento',
        subject='Idx',
        alpha=0.05,
        alternative='two-sided',
        padjust='bonf',
        effsize='cohen',
        return_desc=True
    )

    return anova, posthoc


# QUESTION 2 [ITSELF]
def question2(df: pd.DataFrame):
    """Includes all the logic to answer the second question."""

    # PREPARATION
    bench_df = prepare_df2(df, 'Bench')
    squat_df = prepare_df2(df, 'Squat')
    deadlift_df = prepare_df2(df, 'Deadlift')

    # ASSERTS
    assert_nulls(bench_df, 'Peso', 'Intento')
    assert_nulls(squat_df, 'Peso', 'Intento')
    assert_nulls(deadlift_df, 'Peso', 'Intento')

    # ANALYSIS
    bench_anova, bench_posthoc = analisis(bench_df)
    squat_anova, squat_posthoc = analisis(squat_df)
    deadlift_anova, deadlift_posthoc = analisis(deadlift_df)

    # OUTPUT
    print("- - - - - BENCH ANALYSIS - - - - - ")
    print(bench_anova)
    print(bench_posthoc)

    print("- - - - - SQUAT ANALYSIS  - - - - - ")
    print(squat_anova)
    print(squat_posthoc)

    print("- - - - - DEADLIFT ANALYSIS - - - - - ")
    print(deadlift_anova)
    print(deadlift_posthoc)

    # PLOT
    graphs2(bench_df, squat_df, deadlift_df)

# QUESTION 3

# DF PREPARATION


def prepare_df3(df: pd.DataFrame):
    """Melt the df into long format and then clean."""

    # WIDE DF -> LONG DF
    df3 = df.melt(
        id_vars=['Name', 'Sex', 'Equipment'],
        value_vars=['Bench3bool', 'Squat3bool', 'Deadlift3bool'],
        var_name='Levantamiento',
        value_name='Exito'
    )

    # CONCRET CLEANING
    return df3.dropna(subset=['Exito'])

# FAIL NORMALIZATION BY TOTAL LIFTS
def fail_rate3(df: pd.DataFrame):
    """Calcula en 2 df diferentes el %Fallos sobre los levantamientos totales."""

    # GLOBAL
    fail_global = df.groupby('Levantamiento')['Exito'].apply(
        lambda x: (x == False).mean() * 100).reset_index(name='FailRate')

    # POR SEXO
    fail_sex_df = df.groupby(['Levantamiento', 'Sex'])['Exito'].apply(
        lambda x: (x == False).mean() * 100).reset_index(name='FailRate')

    # POR EQUIPO
    fail_equip_df = df.groupby(['Levantamiento', 'Equipment'])['Exito'].apply(
        lambda x: (x == False).mean() * 100).reset_index(name='FailRate')

    return fail_global, fail_sex_df, fail_equip_df

# QUESTION 3 [ITSELF]
def question3(df: pd.DataFrame):
    """Includes all the logic to answer the first question."""

    # CONCRET CLEANING
    df3 = prepare_df3(df)

    # ASSERTS
    assert_nulls(df3, 'Exito', 'Levantamiento')

    # FAIL RATE
    fail_global, fail_sex_df, fail_equip_df = fail_rate3(df3)

    # PLOT
    graphs3(fail_global, fail_sex_df, fail_equip_df)

# QUESTION 4

# DF PREPARATION
def prepare_df4(df: pd.DataFrame):
    """Divide el dataset por modalidad."""

    bench_only_df = df[~df['Event'].isin(['D', 'S', 'SD'])].dropna(
        subset=['Best3BenchKg']).copy()
    squat_only_df = df[~df['Event'].isin(['D', 'B', 'BD'])].dropna(
        subset=['Best3SquatKg']).copy()
    deadlift_only_df = df[~df['Event'].isin(['B', 'S', 'SB'])].dropna(
        subset=['Best3DeadliftKg']).copy()

    return bench_only_df, squat_only_df, deadlift_only_df

# FAIL NORMALIZATION BY TOTAL LIFTS
def fail_rate4(df: pd.DataFrame):
    """Calculate the %Misses by event type (SBD) over the total lifts."""

    df4b = df.melt(
        id_vars=['Name', 'Event'],
        value_vars=['Bench3bool', 'Squat3bool', 'Deadlift3bool'],
        var_name='Levantamiento',
        value_name='Exito'
    )

    df4b = df4b.groupby(['Levantamiento', 'Event'])['Exito'].apply(lambda x: (x == False).sum(
    ) / x.dropna().count() * 100 if x.dropna().count() > 0 else np.nan).reset_index(name='FailRate')

    return df4b[df4b['FailRate'] > 0]

# QUESTION 4 [ITSELF]
def question4(df: pd.DataFrame):
    """Includes all the logic to answer the forth question."""

    # CONCRET CLEANING
    df4a = df.dropna(subset=['Event']).copy()

    # NEW COLUMNS
    df4a = pseudo_dots(df4a)

    # ASSERT
    assert_nulls(df4a, 'Event', 'Dot_Bench', 'Dot_Squat', 'Dot_Deadlift')

    # SPLIT POR MODALITY
    bench_only_df, squat_only_df, deadlift_only_df = prepare_df4(df4a)

    # FAIL RATE
    df4b = fail_rate4(df4a)

    # PLOT
    graphs4(bench_only_df, squat_only_df, deadlift_only_df, df4b)

# QUESTION 5

# DF PREPARATION
def prepare_df5(df: pd.DataFrame):
    """Melt the df into long format to analyze the success of the 4th attempt."""

    df5 = df.melt(
        id_vars=['Sex'],
        value_vars=['Bench4bool', 'Squat4bool', 'Deadlift4bool'],
        var_name='Levantamiento',
        value_name='Exito'
    )

    return df5.dropna(subset=['Exito'])

# FAIL NORMALIZATION BY TOTAL LIFTS
def success_rate5(df: pd.DataFrame):
    """Calculate the % success by lift and sex."""

    df5 = df.groupby(['Levantamiento', 'Sex'])['Exito'].apply(lambda x: (
        x == True).sum() / x.dropna().count() * 100).reset_index(name='SuccessRate')

    return df5

# PREGUNTA 5 [ITSELF]
def question5(df: pd.DataFrame):
    """Includes all the logic to answer the fifth question."""

    # CONCRET CLEANING
    df5 = prepare_df5(df)

    # ASSERT
    assert_nulls(df5, 'Exito', 'Levantamiento')

    # FAIL RATE
    df5 = success_rate5(df5)

    # PLOT
    graficos5(df5)
