import sys
import pandas as pd # pyright: ignore[reportMissingModuleSource]
from pathlib import Path
import pytest # pyright: ignore[reportMissingImports]

# -------------------- PATH SETUP --------------------
# Add src directory to Python path so modules can be imported correctly
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR / "src"))

# Import functions explicitly (cleaner and safer)
from data_analyzer_first_half import create_calendar, weekday_income, holiday_earnings # pyright: ignore[reportMissingImports]


# -------------------- FIXTURE --------------------
@pytest.fixture
def df():
    """
    Create a small mock DataFrame for testing.

    This avoids relying on external Excel files and ensures tests are fast and reproducible.
    """
    return pd.DataFrame({
        "MONTH_AND_DATE": pd.to_datetime([
            "2024-01-01", "2024-01-02", "2024-01-03"
        ]),
        "PRICE_x": [100, 200, 300]
    })


def test_create_calendar(df):
    """
    Test that create_calendar returns a DatetimeIndex.
    """
    result = create_calendar(df)

    assert isinstance(result, pd.DatetimeIndex), "Wrong return type"
    assert len(result) > 0, "Holiday calendar should not be empty"


def test_weekday_income(df):
    """
    Test that weekday_income returns a valid Series.
    """
    result = weekday_income(df)

    assert isinstance(result, pd.Series), "Wrong return type"
    assert len(result) > 0, "Result should not be empty"


def test_holiday_earnings(df):
    """
    Test that holiday_earnings returns a tuple of two Series.
    """
    result1, result2 = holiday_earnings(df)

    assert isinstance(result1, pd.Series), "First output is not a Series"
    assert isinstance(result2, pd.Series), "Second output is not a Series"

    # Additional sanity checks
    assert len(result1) > 0
    assert len(result2) > 0