import pandas as pd  # pyright: ignore[reportMissingModuleSource]
from mypackage import *  # imports BASE_DIR and excel_checker


def table_merger(df):
    """
    Merge multiple sheets from an Excel file into a single DataFrame.

    Parameters
    ----------
    df : dict[str, pandas.DataFrame]
        Dictionary of DataFrames returned by:
        pd.read_excel(..., sheet_name=None),
        where keys correspond to sheet names.

    Returns
    -------
    pandas.DataFrame
        A merged DataFrame combining relevant information from all sheets.
    """

    # -------------------- EXTRACT SHEETS --------------------
    # Each key corresponds to a sheet in the Excel file
    df_orders = df["orders"]           # Order-level information (ORDERID)
    df_makesuse = df["makes_use"]      # Links dishes to ingredients (DISHID ↔ ID)
    df_ingredients = df["ingredients"] # Ingredient-level information (ID)
    df_dishes = df["dishes"]           # Dish-level information (DISHID)
    df_consist_of = df["consist_of"]   # Links orders to dishes (ORDERID ↔ DISHID)

    # -------------------- MERGE TABLES --------------------
    # Combine all datasets step-by-step using relational joins
    df = pd.merge(df_orders, df_consist_of, on="ORDERID")
    df = pd.merge(df, df_dishes, on="DISHID")
    df = pd.merge(df, df_makesuse, on="DISHID")
    df = pd.merge(df, df_ingredients, on="ID")

    # -------------------- CLEAN COLUMNS --------------------
    # Remove columns not needed for analysis
    df = df.drop(["CUSTOMERID", "WAITERID", "TIP"], axis=1)

    return df


def null_deleter(x):
    """
    Remove rows containing null (NaN) values from a DataFrame.

    Parameters
    ----------
    x : pandas.DataFrame
        Input DataFrame.

    Returns
    -------
    pandas.DataFrame
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


def duplicate_deleter(x):
    """
    Remove duplicate rows from a DataFrame.

    Parameters
    ----------
    x : pandas.DataFrame
        Input DataFrame.

    Returns
    -------
    pandas.DataFrame
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