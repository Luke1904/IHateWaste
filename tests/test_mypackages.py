import sys
import os
import pytest # pyright: ignore[reportMissingImports]
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

sys.path.insert(0, os.path.abspath(BASE_DIR/"src"))

from mypackage import excel_checker # pyright: ignore[reportMissingImports]

def test_excel_checker_valid():
    assert excel_checker("test1.xlsx") is None

def test_excel_checker_invalid():
    with pytest.raises(ValueError, match="Need an excel"):
        excel_checker("test2.xlas")