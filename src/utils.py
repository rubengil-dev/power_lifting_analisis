"""
Helper generic functions and assert cheking.
"""

# IMPORTS
import numpy as np
import pandas as pd
from .config import NEG_COLS, DROP_COLS, REQUIRED_COLS, EXPECTED_TYPES

# FOR CLEANING

## AGE-IMPUTER HELPER
def num_extractor(range_str: str, min_val: int = 14, max_val: int = 80) -> float:
    """
    Convert the age ranges from the two alternative age columns into a float using their mean.
    Bounded between min [14] and max [80] by default.
    """

    nums = range_str.split("-")
    new_age = (int(nums[0]) + int(nums[1])) / 2

    return float(np.clip(new_age, min_val, max_val))

## AGE IMPUTER
def age_imputer(fila: pd.Series) -> float:
    """
    Impute age using AgeClass or BirthYearClass if available.
    Prioritize AgeClass because its range is smaller, therefore improving precision.
    """

    if pd.notna(fila['Age']):                      # If value, gimme it
        return fila['Age']

    else:
        # Prioriza AgeClass sobre BirthYearClass
        variable = fila['AgeClass'] if pd.notna(fila['AgeClass']) else fila['BirthYearClass']

        if pd.isna(variable):                      # If both NaN, gimme NaN
            return np.nan

        else:                                      # If not, gimme average
            return num_extractor(variable)

## WEIGHT IMPUTER
def weight_imputer(fila: pd.Series) -> float:
    """Impute body weight using WeightClassKg if available."""

    if pd.notna(fila['BodyweightKg']):              # If value, gimme it
        return fila['BodyweightKg']
    
    weight = fila['WeightClassKg']
    
    if pd.isna(weight) or weight.startswith('-'):   # If NaN or error [-NN], gimme NaN
        return np.nan
    
    cleaned_weight = weight.rstrip('+').strip()     # Cleaning
    
    if cleaned_weight == '':                        # If empty, gimme NaN
        return np.nan
    
    return float(cleaned_weight)                    # If not, gimme number

## BEST LIFT IMPUTER
def best_imputer(lift1: float, lift2: float, lift3: float, best_lift: float) -> float:
    """Impute the best lift using the 3 attempts if any of them is valid."""

    if pd.notna(best_lift):                         # If value, gimme it
        return best_lift
    
    else:
        # Crea una lista de levantamientos válidos
        lifts = [l for l in [lift1, lift2, lift3] if pd.notna(l) and l > 0]
        
        if lifts:                                   # If any, gimme highest
            return max(lifts)
        
        else:                                       # If not, gimme NaN
            return np.nan

## TOTAL LIFTED IMPUTER
def total_imputer(bench: pd.Series, squat: pd.Series, deadlift: pd.Series, total_lift: pd.Series) -> float:
    """Impute TotalKg by summing the 3 best lifts if all 3 are available."""

    if pd.notna(total_lift):                        # If value, gimme it
        return total_lift
    
    elif pd.notna(bench) and pd.notna(squat) and pd.notna(deadlift):        # If all, gime sum
        return bench + squat + deadlift
    
    else:                                           # If not, gimme NaN
        return np.nan

# ASSERTS

## SEX ASSERT
def sex_assert(col: pd.Series):
    
    assert set(col.cat.categories) == {'M', 'F'}, "Mixed sex hasnt been cleaned propperly."

## PLACE ASSERT
def place_assert(col: pd.Series):
    
    assert 'DD' not in col.cat.categories and 'NS' not in col.cat.categories, "Column PLACE still has 'DD' or 'NS'."

## ASSERT LIFTS
def lift_assert(df: pd.DataFrame):
    
    for col in NEG_COLS:

        assert all(df[col].dropna() > 0), f"Column {col} still has negatives values or 0."

## ASSERT COLUMNS
def required_cols_assert(df: pd.DataFrame):
    asserted_cols = REQUIRED_COLS
    required_cols = [col for col in asserted_cols if col not in df.columns]
    assert not required_cols, f"Columns: {required_cols} hasn't been found."

## ASSERT NO COLUMNS
def removed_cols_assert(df: pd.DataFrame):
    asserted_cols = DROP_COLS + ["AgeClass", "BirthYearClass", "WeightClassKg"]
    removed_cols = [col for col in asserted_cols if col in df.columns]
    assert not removed_cols, f"Columns: {removed_cols} hasn't been deleted properly."

## ASSERT TYPES
def assert_types(df: pd.DataFrame):

    for col, exp_type in EXPECTED_TYPES.items():
        now_type = str(df[col].dtype)
        assert now_type == exp_type, f"{col}: esperado {exp_type}, tiene {now_type}"

## ASSERT BY QUEST ~ CHEQUEA LOS NULOS PARA ESA PREGUNTA CONCRETA
def assert_nulls(df: pd.DataFrame, *cols: str):
    """Verify that the specified columns do not have all their values set to NaN."""

    for col in cols:
        assert df[col].notna().any(), f"Column {col} stil has NaN's."

## GLOBAL ASSERT [ITSELF]
def global_assert(df: pd.DataFrame):
    """Call all assertions required for the global check."""

    sex_assert(df['Sex'])
    place_assert(df['Place'])
    lift_assert(df)
    required_cols_assert(df)
    removed_cols_assert(df)
    assert_types(df)

