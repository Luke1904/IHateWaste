import pandas as pd # type: ignore
import openpyxl # type: ignore
import re

# Path to the Excel dataset
path = "/home/lucap/IE_University_Linux/COMPUTER_PROGRAMMING2/CP2_project/data/cleaned_data.xlsx"

# Load the dataset into a DataFrame
data_frame1 = pd.read_excel(path)

# Validate that the provided file is an Excel file
if not re.search(r'\.xlsx$', path):
    raise ValueError("Need an Excel file (.xlsx)")

# Create deep copies to avoid modifying the original DataFrame
data_frame_1_copy = data_frame1.copy(deep=True)
data_frame_1_copy1 = data_frame1.copy(deep=True)


def mostpopulardishes(data_frame1):
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

    # Group by dish name and count occurrences
    data_frame_most_popular = (
        data_frame1.groupby("NAME_x")
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


def volumeofdishes(data_frame1):
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

    # Extract day of the week from the datetime column
    data_frame1["day_of_week"] = data_frame1["MONTH_AND_DATE"].dt.day_name()

    # Count number of entries per day
    data_frame_dishes = (
        data_frame1.groupby("day_of_week")
        .size()
        .reset_index(name="count")
    )

    # Sort by volume (highest first)
    data_frame_dishes = data_frame_dishes.sort_values(
        by="count", ascending=False
    )

    return data_frame_dishes


# Execute functions
df1 = mostpopulardishes(data_frame_1_copy)
df2 = volumeofdishes(data_frame_1_copy1)