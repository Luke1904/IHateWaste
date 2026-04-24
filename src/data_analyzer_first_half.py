import pandas as pd # pyright: ignore[reportMissingModuleSource]
from pandas.tseries.holiday import USFederalHolidayCalendar # pyright: ignore[reportMissingModuleSource]
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
        A list-like structure of holiday dates between the minimum and maximum
        dates present in the dataset.
    """

    # Determine the time span of the dataset
    start = df["MONTH_AND_DATE"].min()
    end = df["MONTH_AND_DATE"].max()

    # Initialize holiday calendar
    cal = USFederalHolidayCalendar()

    # Generate holidays within the date range
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

    # Create a copy to avoid modifying the original DataFrame
    df_1 = df.copy()

    # Ensure date column is in datetime format
    df_1["MONTH_AND_DATE"] = pd.to_datetime(df_1["MONTH_AND_DATE"])

    # Extract weekday names (Monday, Tuesday, etc.)
    df_1["day"] = df_1["MONTH_AND_DATE"].dt.day_name()

    # Compute average income per weekday
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

    # Generate holiday calendar based on dataset dates
    holidays = create_calendar(df)

    # Create a copy to avoid modifying original data
    df_2 = df.copy()

    # Flag rows that correspond to holidays
    df_2["is_holiday"] = df_2["MONTH_AND_DATE"].isin(holidays)

    # Compute total earnings for holiday vs non-holiday
    result1 = df_2.groupby("is_holiday")["PRICE_x"].sum()
    result1 = result1.sort_values(ascending=False)
    result1 = result1.rename("Holiday vs non-holiday earnings")

    # Compute average earnings for holiday vs non-holiday
    result2 = df_2.groupby("is_holiday")["PRICE_x"].mean()
    result2 = result2.sort_values(ascending=False)
    result2 = result2.rename("Average earnings on either holiday or non-holiday")

    return result1, result2


# Construct path to cleaned dataset
path = BASE_DIR / "data" / "cleaned_data.xlsx"

if __name__ == "__main__":
    # Load the cleaned dataset from the specified Excel file
    # (assumes 'path' has already been defined correctly)
    df = pd.read_excel(path)

    # Compute and display the average income for each weekday
    # This uses the weekday_income function defined earlier
    print(weekday_income(df))

    # Compute and display both:
    # 1. Total earnings on holidays vs non-holidays
    # 2. Average earnings on holidays vs non-holidays
    # The function returns a tuple of two Series, which are printed here
    print(holiday_earnings(df))