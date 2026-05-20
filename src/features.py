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

        df[bool_col] = pd.Series(np.where(df[attempt].isna(), pd.NA, df[attempt] > 0)).astype('boolean')

        return df