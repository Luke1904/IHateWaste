"""
data_cleaner.py
---------------
Provides functions to merge, clean, and deduplicate the raw restaurant
inventory Excel file. Designed to be imported by main_gui.py.
"""

import pandas as pd
from typing import Union


def table_merger(df: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """
    Merge multiple sheets from an Excel file into a single DataFrame.

    Parameters
    ----------
    df : dict[str, pd.DataFrame]
        Dictionary of DataFrames returned by:
        pd.read_excel(..., sheet_name=None),
        where keys correspond to sheet names.

    Returns
    -------
    pd.DataFrame
        A merged DataFrame combining relevant information from all sheets.
    """

    # -------------------- EXTRACT SHEETS --------------------
    # Each key corresponds to a sheet in the Excel file
    df_orders      : pd.DataFrame = df["orders"]       # Order-level information (ORDERID)
    df_makesuse    : pd.DataFrame = df["makes_use"]     # Links dishes to ingredients (DISHID ↔ ID)
    df_ingredients : pd.DataFrame = df["ingredients"]   # Ingredient-level information (ID)
    df_dishes      : pd.DataFrame = df["dishes"]        # Dish-level information (DISHID)
    df_consist_of  : pd.DataFrame = df["consist_of"]    # Links orders to dishes (ORDERID ↔ DISHID)

    # -------------------- MERGE TABLES --------------------
    # Combine all datasets step-by-step using relational joins
    merged: pd.DataFrame = pd.merge(df_orders, df_consist_of, on="ORDERID")
    merged = pd.merge(merged, df_dishes, on="DISHID")
    merged = pd.merge(merged, df_makesuse, on="DISHID")
    merged = pd.merge(merged, df_ingredients, on="ID")

    # -------------------- CLEAN COLUMNS --------------------
    # Remove columns not needed for analysis
    merged = merged.drop(["CUSTOMERID", "WAITERID", "TIP"], axis=1)

    return merged


def null_deleter(x: pd.DataFrame) -> pd.DataFrame:
    """
    Remove rows containing null (NaN) values from a DataFrame.

    Parameters
    ----------
    x : pd.DataFrame
        Input DataFrame.

    Returns
    -------
    pd.DataFrame
        DataFrame with all rows containing NaN values removed.

    Raises
    ------
    TypeError
        If the input is not a pandas DataFrame.
    """

    # Validate input type
    if not isinstance(x, pd.DataFrame):
        raise TypeError("Need pandas dataframe")

    # Drop rows containing any missing values
    return x.dropna()


def duplicate_deleter(x: pd.DataFrame) -> pd.DataFrame:
    """
    Remove duplicate rows from a DataFrame.

    Parameters
    ----------
    x : pd.DataFrame
        Input DataFrame.

    Returns
    -------
    pd.DataFrame
        DataFrame with duplicate rows removed.

    Raises
    ------
    TypeError
        If the input is not a pandas DataFrame.
    """

    # Validate input type
    if not isinstance(x, pd.DataFrame):
        raise TypeError("Need pandas dataframe")

    # Remove duplicate rows
    return x.drop_duplicates()