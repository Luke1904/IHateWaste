import sys
import os
import pandas as pd # type: ignore
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

sys.path.insert(0, os.path.abspath(BASE_DIR/"src"))

from data_cleaner import load_data # type: ignore
from data_cleaner import table_merger # type: ignore
from data_cleaner import null_deleter # type: ignore
from data_cleaner import duplicate_deleter # type: ignore

df1 = load_data()

def test_table_merger():
    result = table_merger(df1)
    assert isinstance(result, pd.DataFrame), "The function doesn't work correctly"

def test_null_deleter():
    result = table_merger(df1)
    result = null_deleter(result)
    assert result.isnull().sum().sum() == 0, "There are still NaNs left in the table"

def test_duplicate_deleter():
    result = table_merger(df1)
    result = duplicate_deleter(result)
    assert result.duplicated().sum() == 0, "There are still duplicates left in the table"