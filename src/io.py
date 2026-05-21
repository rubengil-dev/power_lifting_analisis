"""
Funciones de entrada y salida de datos: carga y guardado de DataFrames.
"""

# IMPORTS
import pandas as pd
from pathlib import Path

# CARGA DEL DF_RAW
def load(path: str | Path) -> pd.DataFrame:
    """Loads a CSV file into a DF."""

    return pd.read_csv(path, low_memory = False)

def save(df: pd.DataFrame, path: str | Path) -> None:
    """Saves a DF into a CSV file."""
    
    df.to_csv(path)