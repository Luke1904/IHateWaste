"""
data_analyzer_first_half.py
---------------------------
Provides functions to analyze earnings trends by weekday and holiday
status. Designed to be imported by main_gui.py.
"""

import pandas as pd
from pandas.tseries.holiday import USFederalHolidayCalendar


def create_calendar(df: pd.DataFrame) -> pd.DatetimeIndex:
    """
    Create a calendar of US federal holidays within the date range of the dataset.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing a datetime column 'MONTH_AND_DATE'.

    Returns
    -------
    pd.DatetimeIndex
        A collection of holiday dates between the minimum and maximum
        dates present in the dataset.
    """

    # -------------------- DATE RANGE EXTRACTION --------------------
    # Identify the earliest and latest dates in the dataset
    start: pd.Timestamp = df["MONTH_AND_DATE"].min()
    end:   pd.Timestamp = df["MONTH_AND_DATE"].max()

    # -------------------- HOLIDAY CALENDAR --------------------
    # Initialize the US Federal Holiday calendar
    cal: USFederalHolidayCalendar = USFederalHolidayCalendar()

    # Generate all holidays within the dataset's date range
    holidays: pd.DatetimeIndex = cal.holidays(start=start, end=end)

    return holidays


def weekday_income(df: pd.DataFrame) -> pd.Series:
    """
    Compute the average income per weekday.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing:
        - 'MONTH_AND_DATE' (date column)
        - 'PRICE_x' (numeric column representing earnings)

    Returns
    -------
    pd.Series
        Series indexed by weekday name, containing average income,
        sorted in descending order.
    """

    # -------------------- DATA PREPARATION --------------------
    # Copy DataFrame to avoid modifying the original
    df_1: pd.DataFrame = df.copy()

    # Ensure the date column is properly formatted as datetime
    df_1["MONTH_AND_DATE"] = pd.to_datetime(df_1["MONTH_AND_DATE"])

    # Extract weekday names (Monday, Tuesday, etc.)
    df_1["day"] = df_1["MONTH_AND_DATE"].dt.day_name()

    # -------------------- AGGREGATION --------------------
    # Compute mean income grouped by weekday
    result: pd.Series = df_1.groupby("day")["PRICE_x"].mean()

    # Sort results in descending order
    result = result.sort_values(ascending=False)

    # Assign a descriptive name to the Series
    result = result.rename("Average income by day")

    return result


def holiday_earnings(df: pd.DataFrame) -> tuple[pd.Series, pd.Series]:
    """
    Compute total and average earnings for holidays vs non-holidays.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing:
        - 'MONTH_AND_DATE' (date column)
        - 'PRICE_x' (numeric earnings column)

    Returns
    -------
    tuple[pd.Series, pd.Series]
        - First Series: total earnings for holiday vs non-holiday
        - Second Series: average earnings for holiday vs non-holiday
    """

    # -------------------- HOLIDAY DETECTION --------------------
    # Generate holiday calendar based on dataset date range
    holidays: pd.DatetimeIndex = create_calendar(df)

    # Create a copy to avoid modifying original data
    df_2: pd.DataFrame = df.copy()

    # Flag rows that fall on holidays
    df_2["is_holiday"] = df_2["MONTH_AND_DATE"].isin(holidays)

    # -------------------- TOTAL EARNINGS --------------------
    result1: pd.Series = df_2.groupby("is_holiday")["PRICE_x"].sum()
    result1 = result1.sort_values(ascending=False)
    result1 = result1.rename("Holiday vs non-holiday earnings")

    # -------------------- AVERAGE EARNINGS --------------------
    result2: pd.Series = df_2.groupby("is_holiday")["PRICE_x"].mean()
    result2 = result2.sort_values(ascending=False)
    result2 = result2.rename("Average earnings on either holiday or non-holiday")

    return result1, result2


# -------------------- EXECUTION BLOCK --------------------
# This ensures the code only runs when the file is executed directly,
# not when imported (important for pytest and modular design)
if __name__ == "__main__":
    from mypackage import BASE_DIR

    # Load the cleaned dataset from the Excel file
    path = BASE_DIR / "data" / "cleaned_data.xlsx"
    df: pd.DataFrame = pd.read_excel(path)

    # Print average income per weekday
    print(weekday_income(df))

    # Print both total and average holiday earnings
    print(holiday_earnings(df))