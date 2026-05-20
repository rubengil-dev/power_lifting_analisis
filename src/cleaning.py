"""
Funciones de limpieza del dataset: duplicados, tipos, nulos y valores inválidos.
"""

# IMPORTS
import numpy as np
import pandas as pd
from config import DROP_COLS, CAT_COLS
from src.utils import age_imputer, weight_imputer, best_imputer, total_imputer

# PRE-FILTRO INICIAL
def pre_filter(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aplica el filtro de criterio y elimina las columnas que no vamos a analizar:
        1. Sólo analizamos competiciones oficiales.
        2. Sólo analizamos competiciones bajo test anti-dopaje.
        3. Sólo se admite al atleta si no fue descalificado en dicha participación.
    """

    # FILTRAR
    df = df[
        (df['Sanctioned'] == 'Yes') & 
        (df['Tested'] == 'Yes') & 
        (df['Place'] != 'DD') & 
        (df['Place'] != 'NS')]
    
    # ELIMINAR COLUMNAS INSERVIBLES
    df = df.drop(columns = DROP_COLS)

    return df

# LIMPIEZA DE DUPLICADOS
def duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Elimina duplicados absolutos"""

    df = df.drop_duplicates()
    
    return df

# LIMPIEZA DE TIPOS
def types(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convierte las columnas a sus tipos correctos, pero lo hace solo sobre columnas definitivas.
    Es decir, columnas que vayan a ser eliminadas no se arreglan.
    Arreglos actuales: Sex -> [Cat], Event -> [Cat], Equipment -> [Cat], Date -> [Date]. 
    """

    # CATEGÓRICAS
    df[CAT_COLS] = df[CAT_COLS].astype('category')

    # FECHAS
    df['Date'] = pd.to_datetime(df['Date'])

    return df

# LIMPIEZA DE NULOS

## LIMPIEZA DE EDAD
def age_cleaner(df: pd.DataFrame) -> pd.DataFrame:
    """Utiliza age_imputer para imputar la edad y después elimina las columnas con las que se ha imputado."""

    # LIMPIA EDAD
    df['Age'] = df.apply(age_imputer, axis=1)

    # ELIMINA COLUMNAS
    df = df.drop(columns=['AgeClass', 'BirthYearClass'])

    return df

## LIMPIEZA DE PESO
def weight_cleaner(df: pd.DataFrame) -> pd.DataFrame:
    """Utiliza weight_imputer para imputar el peso y después elimina la columna con las que se ha imputado."""

    # LIMPIA PESO
    df['BodyweightKg'] = df.apply(weight_imputer, axis=1)

    # ELIMINA COLUMNA
    df = df.drop(columns=['WeightClassKg'])

    return df

## LIMPIEZA DE MEJOR LEVANTAMIENTO
def best_cleaner(df: pd.DataFrame) -> pd.DataFrame:
    """Imputa nulos en Best3Kg usando el máximo de los 3 intentos válidos (mayores que 0) después de chequearlo."""
    
    # COLS A CHEQUEAR
    for best_col, lift_cols in [
        ('Best3BenchKg',    ['Bench1Kg',    'Bench2Kg',    'Bench3Kg']),
        ('Best3SquatKg',    ['Squat1Kg',    'Squat2Kg',    'Squat3Kg']),
        ('Best3DeadliftKg', ['Deadlift1Kg', 'Deadlift2Kg', 'Deadlift3Kg']),
    ]:
        # CHEQUEO
        imputable = df[best_col].isna() & (df[lift_cols] > 0).any(axis=1)
        
        # SI HAY ALGO QUE IMPUTAR, IMPUTA
        if imputable.any():

            df.loc[imputable, best_col] = df[imputable].apply(
                lambda f: best_imputer(
                    f[lift_cols[0]],
                    f[lift_cols[1]],
                    f[lift_cols[2]],
                    f[best_col]),
                    axis=1
                    )
    
    return df

## LIMPIEZA DE TOTAL LEVANTADO
def total_cleaner(df: pd.DataFrame) -> pd.DataFrame:
    """Imputa nulos en TotalKg sumando los 3 best lifts."""

    df['TotalKg'] = df.apply(lambda f: total_imputer(f['Best3BenchKg'], f['Best3SquatKg'], f['Best3DeadliftKg'], f['TotalKg']), axis=1)

    return df

# FINALMENTE, LA FUNCIÓN QUE IMPUTA TODOS LOS NULOS A LA VEZ
def null_imputer(df: pd.DataFrame) -> pd.DataFrame:
    """
    Esta función no limpia TODOS los nulos. Imputa lo que puede a partir de los datos del DF.
    
    DATOS IMPUTADOS: Edad, Peso, Mejor levantamiento y Levantamiento total.
    """

    df = age_cleaner(df)
    df = weight_cleaner(df)
    df = best_cleaner(df)
    df = total_cleaner(df)
    
    return df