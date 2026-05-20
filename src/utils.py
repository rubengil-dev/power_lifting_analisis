"""
Funciones auxiliares genéricas reutilizables por el resto de módulos y comprobaciones tipo assert.
"""

# IMPORTS
import numpy as np
import pandas as pd

# AUXILIAR DE AGE_IMPUTER
def num_extractor(range_str: str, min_val: int = 14, max_val: int = 80) -> float:
    """
    Convierte los rangos de las 2 columnas alternativas de edad en un float con su media.
    Está acotado entre min [14] y max [80] por defecto.
    """

    nums = range_str.split("-")
    new_age = (int(nums[0]) + int(nums[1])) / 2

    return float(np.clip(new_age, min_val, max_val))

# IMPUTER DE EDAD
def age_imputer(fila: pd.Series) -> float:
    """
    Imputa la edad usando AgeClass o BirthYearClass si está disponible.
    Prioriza AgeClass porque su rango es más pequeño y por tanto, mejora la precisión.
    """

    if pd.notna(fila['Age']):                   # Si ya tiene valor, dame ese
        return fila['Age']

    else:
        # Prioriza AgeClass sobre BirthYearClass
        variable = fila['AgeClass'] if pd.notna(fila['AgeClass']) else fila['BirthYearClass']

        if pd.isna(variable):                   # Si ambas son NaN, dame Nan
            return np.nan

        else:                                   # Sino, dame la media del intervalo
            return num_extractor(variable)

# IMPUTER DE PESO
def weight_imputer(fila: pd.Series) -> float:
    """Imputa el peso corporal usando WeightClassKg si está disponible."""

    if pd.notna(fila['BodyweightKg']):          # Si ya tiene valor, dame ese
        return fila['BodyweightKg']
    
    peso = fila['WeightClassKg']
    
    if pd.isna(peso) or peso.startswith('-'):   # Si es NaN o un error [-NN], dame NaN
        return np.nan
    
    return float(peso.rstrip('+'))              # Si no, dame el número a secas

# IMPUTER DE MEJOR LEVANTAMIENTO
def best_imputer(lift1: float, lift2: float, lift3: float, best_lift: float) -> float:
    """Imputa el mejor levantamiento usando los 3 levantamientos si alguno de los 3 es válido."""

    if pd.notna(best_lift):             # Si ya tiene valor, dame ese
        return best_lift
    
    else:
        # Crea una lista de levantamientos válidos
        lifts = [l for l in [lift1, lift2, lift3] if pd.notna(l) and l > 0]
        
        if lifts:                       # Si hay alguno, dame el más alto
            return max(lifts)
        
        else:                           # Sino, dame NaN
            return np.nan

# IMPUTER DE TOTAL LEVANTADO
def total_imputer(bench: pd.Series, squat: pd.Series, deadlift: pd.Series, total_lift: pd.Series) -> float:
    """Imputa TotalKg sumando los 3 best lifts si los 3 están disponibles."""

    if pd.notna(total_lift):                                                # Si ya tiene, dame ese
        return total_lift
    
    elif pd.notna(bench) and pd.notna(squat) and pd.notna(deadlift):        # Si ninguno es NaN, dame la suma
        return bench + squat + deadlift
    
    else:                                                                   # Sino, dame NaN
        return np.nan





def assert_columns(df: pd.DataFrame, required: list[str]) -> None:
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f'Missing columns: {missing}')
