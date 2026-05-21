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

    df = df.copy()

    df4['Dot_Bench'] = df4['Best3BenchKg'] / df4['BodyweightKg']
    df4['Dot_Squat'] = df4['Best3SquatKg'] / df4['BodyweightKg']
    df4['Dot_Deadlift'] = df4['Best3DeadliftKg'] / df4['BodyweightKg']

    return df4