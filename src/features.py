"""
Creación de nuevas columnas derivadas a partir del dataset limpio.
"""

# IMPORTS
import numpy as np
import pandas as pd
from .config import BOOL_COLS


def bool_lift(df: pd.DataFrame) -> pd.DataFrame:
    """
    Crea las columnas booleanas para los 3 y 4 levantamiento en los 3 ejercicios.
    Debe ejecutarse antes de cleaning.fix_data() o no funcionará pues los negativos ya habrán sido limpiados.
    """

    for attempt, bool_col in BOOL_COLS:

        df[bool_col] = pd.Series(np.where(df[attempt].isna(), pd.NA, df[attempt] > 0), dtype = 'boolean', index = df.index)

    return df
    
def pseudo_dots(df: pd.DataFrame):
    """Crea variables de rendimiento relativas al peso corporal ~ Mi pseudo DOTS."""

    df['Dot_Bench'] = df['Best3BenchKg'] / df['BodyweightKg']
    df['Dot_Squat'] = df['Best3SquatKg'] / df['BodyweightKg']
    df['Dot_Deadlift'] = df['Best3DeadliftKg'] / df['BodyweightKg']

    return df