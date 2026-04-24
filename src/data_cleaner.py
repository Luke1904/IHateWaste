import pandas as pd # type: ignore
from mypackage import *

def table_merger(df):

    df_orders = df["orders"] # Order ID
    df_makesuse = df["makes_use"] #Dish ID and ID
    df_ingredients = df["ingredients"] #ID
    df_dishes = df["dishes"] #Dish ID
    df_consist_of = df["consist_of"] #Dish ID and Order ID

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

def load_data():
    path = BASE_DIR / "data" / "github_inventory_unfilltered.xlsx"
    excel_checker(path)
    return pd.read_excel(path, sheet_name=None)

df1 = load_data()
df1 = table_merger(df1)
df1 = null_deleter(df1)
df1 = duplicate_deleter(df1)
df1.to_excel(BASE_DIR / "data" / "cleaned_data.xlsx", index=False)