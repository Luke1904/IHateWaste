import pandas as pd
import numpy as np
import re

path = "/mnt/c/users/djlow/CP2_project/data/github_inventory_unfilltered.xlsx"


def table_merger(df):

    df_orders = df1["orders"] # Order ID
    df_makesuse = df1["makes_use"] #Dish ID and ID
    df_ingredients = df1["ingredients"] #ID
    df_dishes = df1["dishes"] #Dish ID
    df_consist_of = df1["consist_of"] #Dish ID and Order ID

    df = pd.merge(df_orders, df_consist_of, on="ORDERID")
    df = pd.merge(df, df_dishes, on="DISHID")
    df = pd.merge(df, df_makesuse, on="DISHID")
    df = pd.merge(df, df_ingredients, on="ID")

    df = df.drop(["CUSTOMERID", "WAITERID", "TIP"], axis=1)
    
    return df

def null_deleter(x):
    if not isinstance(x, (pd.DataFrame)):
        raise TypeError("Need pandas dataframe")
    return x.dropna()

def duplicate_deleter(x):
    if not isinstance(x, (pd.DataFrame)):
        raise TypeError("Need pandas dataframe")
    return x.drop_duplicates()


if not re.search(r'\.xlsx$', path):
        raise ValueError("Need an excel")

df1 = pd.read_excel(path, sheet_name=None)

df1 = table_merger(df1)
df1 = null_deleter(df1)
df1 = duplicate_deleter(df1)


df1.to_excel("cleaned_data.xlsx", index=False)

print(df1)
