"""
Funciones auxiliares genéricas reutilizables por el resto de módulos y comprobaciones tipo assert.
"""

# IMPORTS
import numpy as np
import pandas as pd


import pandas as pd
def assert_columns(df: pd.DataFrame, required: list[str]) -> None:
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f'Missing columns: {missing}')
