"""
Funciones de entrada y salida de datos: carga y guardado de DataFrames.
"""

# IMPORTS
import pandas as pd
from pathlib import Path
from .config import DISPLAY

# SET-UP DE LOS DISPLAY DE PD
def pd_display():
    """Configura los display para que se vean todas las columnas sin ancho máximo."""

    for key, value in DISPLAY.items():
        pd.set_option(key, value)

# CARGA DEL DF_RAW
def load(path: str | Path) -> pd.DataFrame:
    """Loads a CSV file into a DF."""

    return pd.read_csv(path, low_memory = False)

# GUARDADO DEL DF_CLEAN
def save(df: pd.DataFrame, path: str | Path) -> None:
    """Saves a DF into a CSV file."""
    
    df.to_csv(path, index = False)