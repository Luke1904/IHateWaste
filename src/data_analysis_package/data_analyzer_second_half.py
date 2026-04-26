"""
data_analyzer_second_half.py
----------------------------
Provides functions to analyze dish popularity and volume trends.
Designed to be imported by main_gui.py.
"""

import pandas as pd


def most_popular_dishes(data_frame1: pd.DataFrame) -> pd.DataFrame:
    """
    Compute the most popular dishes based on frequency.

    Parameters
    ----------
    data_frame1 : pd.DataFrame
        Input DataFrame containing a column 'NAME_x' with dish names.

    Returns
    -------
    pd.DataFrame
        DataFrame with:
        - 'Name of dish': unique dish names
        - 'count': number of occurrences of each dish
        Sorted in descending order of popularity.
    """

    # Create a copy to avoid modifying the original DataFrame
    data_frame1_copy: pd.DataFrame = data_frame1.copy()

    # Group by dish name and count occurrences
    data_frame_most_popular: pd.DataFrame = (
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


def volume_of_dishes(data_frame1: pd.DataFrame) -> pd.DataFrame:
    """
    Compute the volume of dishes per day of the week.

    Parameters
    ----------
    data_frame1 : pd.DataFrame
        Input DataFrame containing a datetime column 'MONTH_AND_DATE'.

    Returns
    -------
    pd.DataFrame
        DataFrame with:
        - 'day_of_week': name of the weekday
        - 'count': number of dishes for each day
        Sorted in descending order of volume.
    """

    # Create a copy to avoid modifying the original DataFrame
    data_frame1_copy: pd.DataFrame = data_frame1.copy()

    # Ensure the date column is in datetime format
    data_frame1_copy["MONTH_AND_DATE"] = pd.to_datetime(
        data_frame1_copy["MONTH_AND_DATE"]
    )

    # Extract weekday names (Monday, Tuesday, etc.)
    data_frame1_copy["day_of_week"] = data_frame1_copy["MONTH_AND_DATE"].dt.day_name()

    # Count number of entries per day
    data_frame_dishes: pd.DataFrame = (
        data_frame1_copy.groupby("day_of_week")
        .size()
        .reset_index(name="count")
    )

    # Sort by volume (highest first)
    data_frame_dishes = data_frame_dishes.sort_values(
        by="count", ascending=False
    )

    return data_frame_dishes


def dish_volume_by_day(data_frame1: pd.DataFrame) -> pd.Series:
    """
    Compute the average number of orders per dish per weekday.

    Parameters
    ----------
    data_frame1 : pd.DataFrame
        Input DataFrame containing:
        - 'NAME_x' (dish name)
        - 'MONTH_AND_DATE' (date)
        - 'ORDERID' (order identifier)

    Returns
    -------
    pd.Series
        Multi-index Series indexed by (dish, weekday),
        containing average number of orders, sorted descending.
    """

    # Create a copy to avoid modifying original DataFrame
    data_frame1_copy: pd.DataFrame = data_frame1.copy()

    # Ensure date column is datetime
    data_frame1_copy["MONTH_AND_DATE"] = pd.to_datetime(
        data_frame1_copy["MONTH_AND_DATE"]
    )

    # Extract weekday names
    data_frame1_copy["day_of_week"] = data_frame1_copy["MONTH_AND_DATE"].dt.day_name()

    # Compute average number of orders per dish per weekday
    data_frame_dish_by_day: pd.Series = (
        data_frame1_copy
        .groupby(["NAME_x", "day_of_week"])["ORDERID"]
        .mean()
    )

    # Sort results in descending order
    data_frame_dish_by_day = data_frame_dish_by_day.sort_values(ascending=False)

    # Assign a descriptive name to the Series
    data_frame_dish_by_day = data_frame_dish_by_day.rename("Dish volume by day")

    return data_frame_dish_by_day


# -------------------- EXECUTION BLOCK --------------------
# This ensures the code only runs when the file is executed directly,
# not when imported (important for pytest and modular design)
if __name__ == "__main__":
    from mypackage import BASE_DIR

    path = BASE_DIR / "data" / "cleaned_data.xlsx"
    data_frame1: pd.DataFrame = pd.read_excel(path)

    print(most_popular_dishes(data_frame1))
    print(volume_of_dishes(data_frame1))
    print(dish_volume_by_day(data_frame1))