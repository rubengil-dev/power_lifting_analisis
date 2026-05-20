"""
Creación de nuevas columnas derivadas a partir del dataset limpio.
"""

# IMPORTS
import numpy as np
import pandas as pd
from src.config import BOOL_COLS


def bool_lift(df: pd.DataFrame) -> pd.DataFrame:
    """
    Crea las columnas booleanas para los 3 y 4 levantamiento en los 3 ejercicios.
    Debe ejecutarse antes de cleaning.fix_data() o no funcionará pues los negativos ya habrán sido limpiados.
    """

    for attempt, bool_col in BOOL_COLS:

        df[bool_col] = (df[attempt] > 0).astype('boolean')

        # TERCER INTENTO
        df['Bench3bool'] = np.where(pd.notna(df['Bench3Kg']), np.where(df['Bench3Kg'] > 0, True, False), np.nan)
        df['Squat3bool'] = np.where(pd.notna(df['Squat3Kg']), np.where(df['Squat3Kg'] > 0, True, False), np.nan)
        df['Deadlift3bool'] = np.where(pd.notna(df['Deadlift3Kg']), np.where(df['Deadlift3Kg'] > 0, True, False), np.nan)

        # CUARTO INTENTO
        df['Bench4bool'] = np.where(pd.notna(df['Bench4Kg']), np.where(df['Bench4Kg'] > 0, True, False), np.nan)
        df['Squat4bool'] = np.where(pd.notna(df['Squat4Kg']), np.where(df['Squat4Kg'] > 0, True, False), np.nan)
        df['Deadlift4bool'] = np.where(pd.notna(df['Deadlift4Kg']), np.where(df['Deadlift4Kg'] > 0, True, False), np.nan)

    return df