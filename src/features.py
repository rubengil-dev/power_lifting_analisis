"""
Creación de nuevas columnas derivadas a partir del dataset limpio.
"""

# IMPORTS
import numpy as np
import pandas as pd
from .config import BOOL_COLS


def bool_lift(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create boolean columns for the 3rd and 4th attempts across all 3 lifts.
    Must be executed before cleaning.fix_data(), otherwise it will fail as negatives will have already been cleaned.
    """

    for attempt, bool_col in BOOL_COLS:

        df[bool_col] = pd.Series(np.where(df[attempt].isna(), pd.NA, df[attempt] > 0), dtype = 'boolean', index = df.index)

    return df
    
def pseudo_dots(df: pd.DataFrame):
    """Create performance variables relative to body weight ~ My pseudo-DOTS."""

    df['Dot_Bench'] = df['Best3BenchKg'] / df['BodyweightKg']
    df['Dot_Squat'] = df['Best3SquatKg'] / df['BodyweightKg']
    df['Dot_Deadlift'] = df['Best3DeadliftKg'] / df['BodyweightKg']

    return df