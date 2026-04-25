import sys
from pathlib import Path
import pandas as pd # pyright: ignore[reportMissingModuleSource]
import pytest # pyright: ignore[reportMissingImports]

# -------------------- PATH SETUP --------------------
# Add the 'src' directory to Python path so that project modules can be imported
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR/"src"/"data_analysis_package"))

# Import only required functions (avoid wildcard imports)
from data_analyzer_first_half import create_calendar, weekday_income, holiday_earnings # pyright: ignore[reportMissingImports]


# -------------------- FIXTURE --------------------
@pytest.fixture
def df():
    """
    Provide a small, controlled DataFrame for testing.

    This avoids reliance on external Excel files and ensures tests are:
    - fast
    - reproducible
    - independent of external state
    """
    return pd.DataFrame({
        "MONTH_AND_DATE": pd.to_datetime([
            "2024-01-01",  # New Year's Day (US holiday)
            "2024-01-02",
            "2024-01-03"
        ]),
        "PRICE_x": [100, 200, 300]
    })


# -------------------- TESTS --------------------

def test_create_calendar(df):
    """
    Verify that create_calendar returns a valid DatetimeIndex
    containing at least one holiday within the dataset range.
    """
    result = create_calendar(df)

    # Check correct type
    assert isinstance(result, pd.DatetimeIndex), "Output is not a DatetimeIndex"

    # Check that at least one holiday exists (sanity check)
    assert len(result) > 0, "Holiday calendar should not be empty"

    # Optional: ensure dtype is datetime-like
    assert str(result.dtype).startswith("datetime64")


def test_weekday_income(df):
    """
    Verify that weekday_income returns a properly structured Series.
    """
    result = weekday_income(df)

    # Type check
    assert isinstance(result, pd.Series), "Output is not a pandas Series"

    # Structure check
    assert result.name == "Average income by day", "Series name is incorrect"

    # Data sanity check
    assert len(result) > 0, "Result should not be empty"


def test_holiday_earnings(df):
    """
    Verify that holiday_earnings returns two valid Series
    representing total and average earnings.
    """
    result1, result2 = holiday_earnings(df)

    # Type checks
    assert isinstance(result1, pd.Series), "First output is not a Series"
    assert isinstance(result2, pd.Series), "Second output is not a Series"

    # Ensure index contains expected boolean values (holiday vs non-holiday)
    assert set(result1.index).issubset({True, False}), "Unexpected index values in result1"
    assert set(result2.index).issubset({True, False}), "Unexpected index values in result2"

    # Sanity checks
    assert len(result1) > 0, "Result1 should not be empty"
    assert len(result2) > 0, "Result2 should not be empty"