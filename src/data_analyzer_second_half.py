import pandas as pd
import openpyxl
import re

path = "/home/lucap/IE_University_Linux/COMPUTER_PROGRAMMING2/CP2_project/data/cleaned_data.xlsx"

data_frame1 = pd.read_excel(path)

if not re.search(r'\.xlsx$', path):
        raise ValueError("Need an excel")

print(data_frame1)

def mostpopulardishes(data_frame1):
    data_frame_most_popular = data_frame1.groupby("NAME_x").aggregate({"NAME_x" : "count"})
    print(data_frame_most_popular.columns)
    print(data_frame_most_popular)

mostpopulardishes(data_frame1)