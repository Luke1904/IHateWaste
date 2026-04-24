import pandas as pd  # pyright: ignore[reportMissingModuleSource]
from pandas.tseries.holiday import USFederalHolidayCalendar  # pyright: ignore[reportMissingModuleSource]
from mypackage import *  # imports BASE_DIR and excel_checker


def create_calendar(df):
    """
    Create a calendar of US federal holidays within the date range of the dataset.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame containing a datetime column 'MONTH_AND_DATE'.

    Returns
    -------
    pandas.DatetimeIndex
        A collection of holiday dates between the minimum and maximum
        dates present in the dataset.
    """

    # -------------------- DATE RANGE EXTRACTION --------------------
    # Identify the earliest and latest dates in the dataset
    start = df["MONTH_AND_DATE"].min()
    end = df["MONTH_AND_DATE"].max()

    # -------------------- HOLIDAY CALENDAR --------------------
    # Initialize the US Federal Holiday calendar
    cal = USFederalHolidayCalendar()

    # Generate all holidays within the dataset's date range
    holidays = cal.holidays(start=start, end=end)

    return holidays


def weekday_income(df):
    """
    Compute the average income per weekday.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame containing:
        - 'MONTH_AND_DATE' (date column)
        - 'PRICE_x' (numeric column representing earnings)

    Returns
    -------
    pandas.Series
        Series indexed by weekday name, containing average income,
        sorted in descending order.
    """

    # -------------------- DATA PREPARATION --------------------
    # Copy DataFrame to avoid modifying the original
    df_1 = df.copy()

    # Ensure the date column is properly formatted as datetime
    df_1["MONTH_AND_DATE"] = pd.to_datetime(df_1["MONTH_AND_DATE"])

    # Extract weekday names (Monday, Tuesday, etc.)
    df_1["day"] = df_1["MONTH_AND_DATE"].dt.day_name()

    # -------------------- AGGREGATION --------------------
    # Compute mean income grouped by weekday
    result = df_1.groupby("day")["PRICE_x"].mean()

    # Sort results in descending order
    result = result.sort_values(ascending=False)

    # Assign a descriptive name to the Series
    result = result.rename("Average income by day")

    return result


def holiday_earnings(df):
    """
    Compute total and average earnings for holidays vs non-holidays.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame containing:
        - 'MONTH_AND_DATE' (date column)
        - 'PRICE_x' (numeric earnings column)

    Returns
    -------
    tuple[pandas.Series, pandas.Series]
        - First Series: total earnings for holiday vs non-holiday
        - Second Series: average earnings for holiday vs non-holiday
    """

    # -------------------- HOLIDAY DETECTION --------------------
    # Generate holiday calendar based on dataset date range
    holidays = create_calendar(df)

    # Create a copy to avoid modifying original data
    df_2 = df.copy()

    # Flag rows that fall on holidays
    df_2["is_holiday"] = df_2["MONTH_AND_DATE"].isin(holidays)

    # -------------------- TOTAL EARNINGS --------------------
    result1 = df_2.groupby("is_holiday")["PRICE_x"].sum()
    result1 = result1.sort_values(ascending=False)
    result1 = result1.rename("Holiday vs non-holiday earnings")

    # -------------------- AVERAGE EARNINGS --------------------
    result2 = df_2.groupby("is_holiday")["PRICE_x"].mean()
    result2 = result2.sort_values(ascending=False)
    result2 = result2.rename("Average earnings on either holiday or non-holiday")

    return result1, result2


# -------------------- DATA PATH --------------------
# Define path to the cleaned dataset
path = BASE_DIR / "data" / "cleaned_data.xlsx"


# -------------------- EXECUTION BLOCK --------------------
# This ensures the code only runs when the file is executed directly,
# not when imported (important for pytest and modular design)
if __name__ == "__main__":

    # Load the cleaned dataset from the Excel file
    df = pd.read_excel(path)

    # -------------------- ANALYSIS OUTPUT --------------------
    # Print average income per weekday
    print(weekday_income(df))

    # Print both total and average holiday earnings
    print(holiday_earnings(df))