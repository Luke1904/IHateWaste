import pandas as pd # pyright: ignore[reportMissingModuleSource]
from mypackage import *  # imports BASE_DIR and excel_checker from your package


def table_merger(df):
    """
    Merge multiple sheets from the Excel file into a single DataFrame.

    Parameters
    ----------
    df : dict[str, pandas.DataFrame]
        Dictionary of DataFrames returned by pd.read_excel(..., sheet_name=None),
        where keys are sheet names.

    Returns
    -------
    pandas.DataFrame
        A merged DataFrame combining relevant information from all sheets.
    """

    # Extract individual sheets from the dictionary
    df_orders = df["orders"]          # Contains ORDERID and order-level data
    df_makesuse = df["makes_use"]     # Links dishes to ingredients (DISHID ↔ ID)
    df_ingredients = df["ingredients"]  # Contains ingredient IDs
    df_dishes = df["dishes"]          # Contains dish information (DISHID)
    df_consist_of = df["consist_of"]  # Links orders to dishes (ORDERID ↔ DISHID)

    # Perform successive merges to combine all relevant tables
    df = pd.merge(df_orders, df_consist_of, on="ORDERID")
    df = pd.merge(df, df_dishes, on="DISHID")
    df = pd.merge(df, df_makesuse, on="DISHID")
    df = pd.merge(df, df_ingredients, on="ID")

    # Drop columns that are not needed for further analysis
    df = df.drop(["CUSTOMERID", "WAITERID", "TIP"], axis=1)

    return df


def null_deleter(x):
    """
    Remove rows containing null values from a DataFrame.

    Parameters
    ----------
    x : pandas.DataFrame

    Returns
    -------
    pandas.DataFrame
        DataFrame with all rows containing NaN values removed.
    """

    # Ensure the input is a DataFrame
    if not isinstance(x, pd.DataFrame):
        raise TypeError("Need pandas dataframe")

    # Drop rows with any missing values
    return x.dropna()


def duplicate_deleter(x):
    """
    Remove duplicate rows from a DataFrame.

    Parameters
    ----------
    x : pandas.DataFrame

    Returns
    -------
    pandas.DataFrame
        DataFrame with duplicate rows removed.
    """

    # Ensure the input is a DataFrame
    if not isinstance(x, pd.DataFrame):
        raise TypeError("Need pandas dataframe")

    # Drop duplicate rows
    return x.drop_duplicates()