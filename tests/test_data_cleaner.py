import sys
import pandas as pd # pyright: ignore[reportMissingModuleSource]
from pathlib import Path
import pytest # pyright: ignore[reportMissingImports]


BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR / "src" / "data_cleaner_package"))

from data_cleaner import table_merger, null_deleter, duplicate_deleter # pyright: ignore[reportMissingImports]


@pytest.fixture
def sheets():
    """
    Create mock Excel data (dictionary of DataFrames)
    matching the structure expected by table_merger.
    """

    return {
        "orders": pd.DataFrame({
            "ORDERID": [1, 2],
            "CUSTOMERID": [10, 20],
            "WAITERID": [100, 200],
            "TIP": [1.5, 2.0]
        }),
        "consist_of": pd.DataFrame({
            "ORDERID": [1, 2],
            "DISHID": [11, 12]
        }),
        "dishes": pd.DataFrame({
            "DISHID": [11, 12],
            "NAME_x": ["Pizza", "Burger"]
        }),
        "makes_use": pd.DataFrame({
            "DISHID": [11, 12],
            "ID": [101, 102]
        }),
        "ingredients": pd.DataFrame({
            "ID": [101, 102]
        })
    }


@pytest.fixture
def merged_df(sheets):
    """
    Apply table_merger to mock data.
    """
    return table_merger(sheets)


def test_table_merger(merged_df):
    """
    Check that merging produces a valid DataFrame.
    """
    assert isinstance(merged_df, pd.DataFrame)
    assert len(merged_df) > 0


def test_null_deleter(merged_df):
    """
    Check that null values are removed.
    """
    result = null_deleter(merged_df)
    assert result.isnull().sum().sum() == 0


def test_duplicate_deleter(merged_df):
    """
    Check that duplicates are removed.
    """
    result = duplicate_deleter(merged_df)
    assert result.duplicated().sum() == 0