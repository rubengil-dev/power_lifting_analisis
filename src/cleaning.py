"""
Dataset cleaning functions: duplicates, types, nulls, and invalid values.
"""

# IMPORTS
import numpy as np
import pandas as pd
from .config import DROP_COLS, CAT_COLS, NEG_COLS, LIFT_COLS
from .utils import age_imputer, weight_imputer, best_imputer, total_imputer

# INITIAL PRE-FILTER
def pre_filter(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply filtering criteria and drop columns that will not be analyzed:
        1. Only analyze official competitions.
        2. Only analyze drug-tested competitions.
        3. Only include the athlete if they were not disqualified in that specific event.
    """

    # FILTER
    df = df[
        (df['Sanctioned'] == 'Yes') & 
        (df['Tested'] == 'Yes') & 
        (df['Place'] != 'DD') & 
        (df['Place'] != 'NS')]
    
    # DELETE USELESS COLUMNS
    df = df.drop(columns = DROP_COLS)

    return df

# DUPLICATES REMOVAL
def duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Removes absolute duplicates."""

    df = df.drop_duplicates()
    
    return df

# TYPE CASTING
def fix_types(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert columns to their correct data types, but only for final columns.
    Columns scheduled to be dropped are ignored.
    Current fixes: Sex -> [Cat], Event -> [Cat], Equipment -> [Cat], Date -> [Date].
    """

    # CATEGORIES
    df[CAT_COLS] = df[CAT_COLS].astype('category')
    
    # DELETE USELESS CATEGORIES
    df['Place'] = df['Place'].cat.remove_unused_categories()

    # DATES
    df['Date'] = pd.to_datetime(df['Date'])

    return df

# NULL CLEANING

## AGE CLEANING
def age_cleaner(df: pd.DataFrame) -> pd.DataFrame:
    """Use age_imputer to impute the age and then drop the columns used for the imputation."""

    # AGE CLEANING ITSELF
    df['Age'] = df.apply(age_imputer, axis=1)

    # REMOVING USED COLUMNS
    df = df.drop(columns = ['AgeClass', 'BirthYearClass'])

    return df

## WEIGHT CLEANER
def weight_cleaner(df: pd.DataFrame) -> pd.DataFrame:
    """Use weight_imputer to impute the weight and then drop the column used for the imputation."""

    # WEIGHT CLEANING ITSELF
    df['BodyweightKg'] = df.apply(weight_imputer, axis=1)

    # REMOVING USED COLUMN
    df = df.drop(columns = ['WeightClassKg'])

    return df

## BEST LIFT CLEANER
def best_cleaner(df: pd.DataFrame) -> pd.DataFrame:
    """Impute nulls in Best3Kg using the maximum of the 3 valid attempts (greater than 0) after checking."""
    
    # COLS TO CHECK
    for best_col, lift_cols in LIFT_COLS:

        # CHECK
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

## TOTAL LIFTED CLEANING
def total_cleaner(df: pd.DataFrame) -> pd.DataFrame:
    """Impute nulls in TotalKg by summing the 3 best lifts."""

    df['TotalKg'] = df.apply(lambda f: total_imputer(f['Best3BenchKg'], f['Best3SquatKg'], f['Best3DeadliftKg'], f['TotalKg']), axis=1)

    return df

# FULL-IMPUTING FUNCTION
def null_imputer(df: pd.DataFrame) -> pd.DataFrame:
    """
    This function does not clean ALL nulls. It imputes what it can based on the dataframe data.

    IMPUTED DATA: Age, Weight, Best lift, and Total lift.
    """

    df = age_cleaner(df)
    df = weight_cleaner(df)
    df = best_cleaner(df)
    df = total_cleaner(df)
    
    return df

# DATA CLEANING

## SEX CLEANING
def sex_cleaner(df: pd.DataFrame) -> pd.DataFrame:
    """Filter the DF to remove mixed sex and drop that category."""

    # FILTER
    df = df[df['Sex'] != 'Mx'].copy()         # .copy is to prevent 'SettingWithCopyWarning'

    # REMOVING FILTERED CATEGORY
    df['Sex'] = df['Sex'].cat.remove_unused_categories()

    return df

## LIFTS CLEANING
def lift_cleaner(df: pd.DataFrame, lifts: list = NEG_COLS) -> pd.DataFrame:
    """Convert negative values [misses] of the lifts into NaN so they are removed during filtering."""

    for lift in lifts:
        df.loc[df[lift] <= 0, lift] = np.nan

    return df

# FULL-CLEANING FUNCTION
def fix_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    This function fixes ALL nonsense values in the DF.

    CLEANED DATA: Mixed sex and negative values in the lifts.
    """

    df = sex_cleaner(df)
    df = lift_cleaner(df)
    
    return df