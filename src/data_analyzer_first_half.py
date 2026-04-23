import pandas as pd # type: ignore
import re
from pandas.tseries.holiday import USFederalHolidayCalendar     # type: ignore # for use in accounting for holidays
from mypackage import *

def create_calendar(df):
        """
        Creating the calendar for holidays. It is necessary to include a start and end date to this calendar.
        """
        start = df["MONTH_AND_DATE"].min()
        end = df["MONTH_AND_DATE"].max()
        cal = USFederalHolidayCalendar()
        holidays = cal.holidays(start=start, end=end)
        return holidays

def weekday_income(x):
        """
        weekday_income takes the dataframe and outputs the average money made in each weekday in descending order
         """
        x = x.copy()
        x["MONTH_AND_DATE"] = pd.to_datetime(x["MONTH_AND_DATE"])       # makes sure that the inserted date column is datetime
        x["day"] = x["MONTH_AND_DATE"].dt.day_name()   # gives the day of the week
        result = x.groupby("day")["PRICE_x"].mean()     # groups daily income by weekday
        result = result.sort_values(ascending=False)    # returns it in descending order
        result = result.rename("Average income by day")
        return result

def holiday_earnings(x):
        """
        holiday_earnings takes the holiday calendar we defined earlier and examines earnings on holidays
        """
        holidays = create_calendar(x)
        x = x.copy()
        x["is_holiday"] = x["MONTH_AND_DATE"].isin(holidays)  # flags holidays
        result1 = x.groupby("is_holiday")["PRICE_x"].sum()      # this is for the aggregated income on either holidays or non-holidays
        result1 = result1.sort_values(ascending=False)
        result1 = result1.rename("Holiday vs non-holiday earnings")
        result2 = x.groupby("is_holiday")["PRICE_x"].mean()     # this is for the average income on either holidays or non-holidays
        result2 = result2.sort_values(ascending=False)
        result2 = result2.rename("Average earnings on either holiday or non-holiday")
        return result1, result2

def run_code():
        path = BASE_DIR/"data"/"cleaned_data.xlsx"      # imports defined object from mypackage
        excel_checker(path)     # calls function from package to check if the path is of the right file type
        df = pd.read_excel(path)
        h_earnings = create_calendar(df)