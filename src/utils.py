"""
Funciones auxiliares genéricas reutilizables por el resto de módulos y comprobaciones tipo assert.
"""

# IMPORTS
import numpy as np
import pandas as pd
from .config import NEG_COLS, DROP_COLS, REQUIRED_COLS, EXPECTED_TYPES

# PARA LA LIMPIEZA

## AUXILIAR DE AGE_IMPUTER
def num_extractor(range_str: str, min_val: int = 14, max_val: int = 80) -> float:
    """
    Convierte los rangos de las 2 columnas alternativas de edad en un float con su media.
    Está acotado entre min [14] y max [80] por defecto.
    """

    nums = range_str.split("-")
    new_age = (int(nums[0]) + int(nums[1])) / 2

    return float(np.clip(new_age, min_val, max_val))

## IMPUTER DE EDAD
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

## IMPUTER DE PESO
def weight_imputer(fila: pd.Series) -> float:
    """Imputa el peso corporal usando WeightClassKg si está disponible."""

    if pd.notna(fila['BodyweightKg']):          # Si ya tiene valor, dame ese
        return fila['BodyweightKg']
    
    peso = fila['WeightClassKg']
    
    if pd.isna(peso) or peso.startswith('-'):   # Si es NaN o un error [-NN], dame NaN
        return np.nan
    
    peso_limpio = peso.rstrip('+').strip()      # Limpiamos
    
    if peso_limpio == '':                       # Si al limpiar se quedó vacío, devuelve NaN
        return np.nan
    
    return float(peso_limpio)                   # Si no, dame el número

## IMPUTER DE MEJOR LEVANTAMIENTO
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

## IMPUTER DE TOTAL LEVANTADO
def total_imputer(bench: pd.Series, squat: pd.Series, deadlift: pd.Series, total_lift: pd.Series) -> float:
    """Imputa TotalKg sumando los 3 best lifts si los 3 están disponibles."""

    if pd.notna(total_lift):                                                # Si ya tiene, dame ese
        return total_lift
    
    elif pd.notna(bench) and pd.notna(squat) and pd.notna(deadlift):        # Si ninguno es NaN, dame la suma
        return bench + squat + deadlift
    
    else:                                                                   # Sino, dame NaN
        return np.nan

# ASSERTS

## ASSERT SEXO
def assert_sexo(columna: pd.Series):
    
    assert set(columna.cat.categories) == {'M', 'F'}, "El sexo mixto no se ha eliminado correctamente."

## ASSERT PLACE
def assert_place(columna: pd.Series):
    
    assert 'DD' not in columna.cat.categories and 'NS' not in columna.cat.categories, "La columna place sigue teniendo 'DD' o 'NS'."

## ASSERT LEVANTAMIENTOS
def assert_levantamientos(df: pd.DataFrame):
    
    for col in NEG_COLS:

        assert all(df[col].dropna() > 0), f"La columna {col} aún tiene valores negativos o 0."

## ASSERT COLUMNS
def assert_required_cols(df: pd.DataFrame):
    asserted_cols = REQUIRED_COLS
    required_cols = [col for col in asserted_cols if col not in df.columns]
    assert not required_cols, f"Las columnas: {required_cols} no se han encontrado."

## ASSERT NO COLUMNS
def assert_removed_cols(df: pd.DataFrame):
    asserted_cols = DROP_COLS + ["AgeClass", "BirthYearClass", "WeightClassKg"]
    removed_cols = [col for col in asserted_cols if col in df.columns]
    assert not removed_cols, f"Las columnas: {removed_cols} no han sido eliminadas correctamente."

## ASSERT TIPOS
def assert_types(df: pd.DataFrame):

    for col, exp_type in EXPECTED_TYPES.items():
        now_type = str(df[col].dtype)
        assert now_type == exp_type, f"{col}: esperado {exp_type}, tiene {now_type}"

## ASSERT POR PREGUNTA ~ CHEQUEA LOS NULOS PARA ESA PREGUNTA CONCRETA
def assert_nulls(df: pd.DataFrame, *cols: str):
    """Comprueba que las columnas indicadas no tienen todos los valores a NaN."""

    for col in cols:
        assert df[col].notna().any(), f"La columna {col} está completamente vacía."

## ASSERT GLOBAL [ITSELF]
def global_assert(df: pd.DataFrame):
    """Llama a todos los asserts necesarios para el check global."""

    assert_sexo(df['Sex'])
    assert_place(df['Place'])
    assert_levantamientos(df)
    assert_required_cols(df)
    assert_removed_cols(df)
    assert_types(df)

