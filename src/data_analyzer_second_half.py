import pandas as pd  # pyright: ignore[reportMissingModuleSource]
from mypackage import *
import re

def most_popular_dishes(data_frame1):
    """
    Compute the most popular dishes based on frequency.

    Parameters
    ----------
    data_frame1 : pandas.DataFrame
        Input DataFrame containing a column 'NAME_x' with dish names.

    Returns
    -------
    pandas.DataFrame
        DataFrame with:
        - 'Name of dish': unique dish names
        - 'count': number of occurrences of each dish
        Sorted in descending order of popularity.
    """
    # Makes copy so as to not mutate original dataframe
    data_frame1_copy = data_frame1.copy()
    # Group by dish name and count occurrences
    data_frame_most_popular = (
        data_frame1_copy.groupby("NAME_x")
        .size()
        .reset_index(name="count")
    )
    # Rename column for readability
    data_frame_most_popular.rename(
        columns={"NAME_x": "Name of dish"},
        inplace=True
    )
    # Sort dishes by popularity (highest first)
    data_frame_most_popular = data_frame_most_popular.sort_values(
        by="count", ascending=False
    )
    return data_frame_most_popular

def volume_of_dishes(data_frame1):
    """
    Compute the volume of dishes per day of the week.

    Parameters
    ----------
    data_frame1 : pandas.DataFrame
        Input DataFrame containing a datetime column 'MONTH_AND_DATE'.

    Returns
    -------
    pandas.DataFrame
        DataFrame with:
        - 'day_of_week': name of the weekday
        - 'count': number of dishes for each day
        Sorted in descending order of volume.
    """
    # Makes copy so as to not mutate original dataframe
    data_frame1_copy = data_frame1.copy()
    # Extract day of the week from the datetime column
    data_frame1_copy["day_of_week"] = data_frame1_copy["MONTH_AND_DATE"].dt.day_name()
    # Count number of entries per day
    data_frame_dishes = (
        data_frame1_copy.groupby("day_of_week")
        .size()
        .reset_index(name="count")
    )
    # Sort by volume (highest first)
    data_frame_dishes = data_frame_dishes.sort_values(
        by="count", ascending=False
    )
    return data_frame_dishes

def dish_volume_by_day(data_frame1):
    # Makes copy so as to not mutate original dataframe
    data_frame1_copy = data_frame1.copy()
    # Create a column for day of the week (monday,tuesday,etc.)
    data_frame1_copy["day_of_week"] = data_frame1_copy["MONTH_AND_DATE"].dt.day_name()
    data_frame_dish_by_day = data_frame1_copy.groupby(["NAME_x", "day_of_week"])["ORDERID"].mean()
    data_frame_dish_by_day = data_frame_dish_by_day.sort_values(ascending=False)    # returns it in descending order
    data_frame_dish_by_day = data_frame_dish_by_day.rename("Dish volume by day")
    return data_frame_dish_by_day

path = BASE_DIR/"data"/"cleaned_data.xlsx"      # imports defined object from mypackage
excel_checker(path)     # calls function from package to check if the path is of the right file type
data_frame1 = pd.read_excel(path)       # Load the dataset into a DataFrame