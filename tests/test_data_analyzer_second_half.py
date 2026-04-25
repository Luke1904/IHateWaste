import sys
import pandas as pd # pyright: ignore[reportMissingModuleSource]
import pytest # pyright: ignore[reportMissingImports]
from pathlib import Path

# -------------------- PATH SETUP --------------------
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR / "src" / "data_analysis_package"))

# -------------------- FIXTURE --------------------
@pytest.fixture
def mock_df():
    """
    Small mock dataset mimicking cleaned data structure.
    """
    return pd.DataFrame({
        "ORDERID": [1, 2, 3, 3],
        "MONTH_AND_DATE": pd.to_datetime([
            "2024-01-01",
            "2024-01-02",
            "2024-01-03",
            "2024-01-03"
        ]),
        "DISHID": [10, 11, 10, 10],
        "NAME_x": ["Pizza", "Burger", "Pizza", "Pizza"],
        "PRICE_x": [10.0, 20.0, 15.0, 15.0],
        "TYPEOFCUISINE": ["Italian", "Fast Food", "Italian", "Italian"],
        "ID": [100, 101, 100, 100],
        "NAME_y": ["Tomato", "Beef", "Tomato", "Tomato"],
        "PRICE_y": [1.0, 2.0, 1.0, 1.0],
        "SUPPLIERID": [500, 501, 500, 500]
    })

# -------------------- IMPORTS --------------------
from data_analyzer_second_half import ( # pyright: ignore[reportMissingImports]
    most_popular_dishes,
    volume_of_dishes,
    dish_volume_by_day
)

# -------------------- TESTS --------------------

def test_most_popular_dishes(mock_df):
    result = most_popular_dishes(mock_df)

    assert isinstance(result, pd.DataFrame)
    assert "Name of dish" in result.columns
    assert "count" in result.columns
    assert result["count"].max() >= 1


def test_volume_of_dishes(mock_df):
    result = volume_of_dishes(mock_df)

    assert isinstance(result, pd.DataFrame)
    assert "day_of_week" in result.columns
    assert "count" in result.columns
    assert len(result) > 0


def test_dish_volume_by_day(mock_df):
    result = dish_volume_by_day(mock_df)

    assert isinstance(result, pd.Series)
    assert result.name == "Dish volume by day"
    assert len(result) > 0