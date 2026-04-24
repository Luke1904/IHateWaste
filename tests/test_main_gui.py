import sys
from pathlib import Path
import pandas as pd # pyright: ignore[reportMissingModuleSource]
import pytest # pyright: ignore[reportMissingImports]

# Add src path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR / "src"))

# Import logic functions (not GUI widgets)
from data_cleaner import table_merger, null_deleter, duplicate_deleter # pyright: ignore[reportMissingImports]
from data_analyzer_first_half import weekday_income, holiday_earnings # pyright: ignore[reportMissingImports]
from data_analyzer_second_half import most_popular_dishes, volume_of_dishes, dish_volume_by_day # pyright: ignore[reportMissingImports]


# -------------------- FIXTURE --------------------
@pytest.fixture
def sample_df():
    """
    Small test DataFrame for analysis functions.
    """
    return pd.DataFrame({
        "NAME_x": ["Pizza", "Burger", "Pizza"],
        "MONTH_AND_DATE": pd.to_datetime([
            "2024-01-01", "2024-01-02", "2024-01-03"
        ]),
        "PRICE_x": [100, 200, 150],
        "ORDERID": [1, 2, 3]
    })


# -------------------- TESTS --------------------

def test_weekday_income(sample_df):
    result = weekday_income(sample_df)
    assert isinstance(result, pd.Series)
    assert len(result) > 0


def test_holiday_earnings(sample_df):
    result1, result2 = holiday_earnings(sample_df)
    assert isinstance(result1, pd.Series)
    assert isinstance(result2, pd.Series)


def test_most_popular_dishes(sample_df):
    result = most_popular_dishes(sample_df)
    assert isinstance(result, pd.DataFrame)
    assert "count" in result.columns


def test_volume_of_dishes(sample_df):
    result = volume_of_dishes(sample_df)
    assert isinstance(result, pd.DataFrame)
    assert "count" in result.columns


def test_dish_volume_by_day(sample_df):
    result = dish_volume_by_day(sample_df)
    assert isinstance(result, pd.Series)