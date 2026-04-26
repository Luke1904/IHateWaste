import sys
from pathlib import Path
import pandas as pd # pyright: ignore[reportMissingModuleSource]
import pytest # pyright: ignore[reportMissingImports]
from unittest.mock import patch

# Add src to path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR / "src"))

# Import only logic functions (NOT GUI)
from data_cleaner_package.data_cleaner import table_merger, null_deleter, duplicate_deleter # pyright: ignore[reportMissingImports]
from data_analysis_package.data_analyzer_first_half import weekday_income, holiday_earnings # pyright: ignore[reportMissingImports]
from data_analysis_package.data_analyzer_second_half import most_popular_dishes, volume_of_dishes, dish_volume_by_day # pyright: ignore[reportMissingImports]


# -------------------- FIXTURE --------------------
@pytest.fixture
def mock_sheets():
    """
    Mock Excel sheet structure used by run_clean().
    """
    return {
        "orders": pd.DataFrame({
            "ORDERID": [1],
            "CUSTOMERID": [10],
            "WAITERID": [100],
            "TIP": [1.5]
        }),
        "consist_of": pd.DataFrame({
            "ORDERID": [1],
            "DISHID": [10]
        }),
        "dishes": pd.DataFrame({
            "DISHID": [10],
            "NAME_x": ["Pizza"]
        }),
        "makes_use": pd.DataFrame({
            "DISHID": [10],
            "ID": [100]
        }),
        "ingredients": pd.DataFrame({
            "ID": [100]
        })
    }


# -------------------- TEST --------------------

def test_clean_pipeline(mock_sheets):
    """
    Test full cleaning pipeline logic.
    """
    df = table_merger(mock_sheets)
    df = null_deleter(df)
    df = duplicate_deleter(df)

    assert isinstance(df, pd.DataFrame)
    assert df.isnull().sum().sum() == 0
    assert df.duplicated().sum() == 0


@patch("pandas.read_excel")
def test_run_clean_logic(mock_read_excel, mock_sheets):
    """
    Mock file loading to test run_clean without GUI interaction.
    """
    mock_read_excel.return_value = mock_sheets

    from main_gui import run_clean, cleaned_df # pyright: ignore[reportMissingImports]

    # simulate selected file
    from main_gui import file_path # pyright: ignore[reportMissingImports]
    file_path.set("dummy.xlsx")

    run_clean()

    assert cleaned_df is not None