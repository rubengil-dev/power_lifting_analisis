"""
Uploading and saving data functions.
"""

# IMPORTS
import pandas as pd
from pathlib import Path
from .config import DISPLAY

# PANDAS DISPLAY SET-UP
def pd_display():
    """Configure display settings to show all columns with no maximum width."""

    for key, value in DISPLAY.items():
        pd.set_option(key, value)

# RAW UPLOAD
def load(path: str | Path) -> pd.DataFrame:
    """Loads a CSV file into a DF."""

    return pd.read_csv(path, low_memory = False)

# CLEAN SAVE
def save(df: pd.DataFrame, path: str | Path) -> None:
    """Saves a DF into a CSV file."""
    
    df.to_csv(path, index = False)