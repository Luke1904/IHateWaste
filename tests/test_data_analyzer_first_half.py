import sys
import os
import pandas as pd # type: ignore
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

sys.path.insert(0, os.path.abspath(BASE_DIR/"src"))

from data_analyzer_first_half import * # type: ignore
from data_analyzer_first_half import df # type: ignore
from data_analyzer_first_half import create_calendar # type: ignore
from data_analyzer_first_half import weekday_income # type: ignore
from data_analyzer_first_half import holiday_earnings  # type: ignore

def test_create_calendar():
    assert type(create_calendar(df)) == pd.core.indexes.datetimes.DatetimeIndex, "It is the wrong data type"

def test_weekday_income():
    assert type(weekday_income(df)) == pd.Series, "It is the wrong data type"

def test_holiday_earnings():
    assert type(holiday_earnings(df)) == tuple, "It is the wrong data type"