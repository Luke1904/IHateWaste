import sys
import os
import pandas as pd # type: ignore
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

sys.path.insert(0, os.path.abspath(BASE_DIR/"src"))

from data_analyzer_second_half import * # type: ignore
from data_analyzer_second_half import data_frame1 # type: ignore
from data_analyzer_second_half import most_popular_dishes # type: ignore
from data_analyzer_second_half import volume_of_dishes # type: ignore
from data_analyzer_second_half import dish_volume_by_day  # type: ignore

def test_most_popular_dishes():
    assert type(most_popular_dishes(data_frame1)) == pd.DataFrame, "It is the wrong data type"

def test_volume_of_dishes():
    assert type(volume_of_dishes(data_frame1)) == pd.DataFrame, "It is the wrong data type"

def test_dish_volume_by_day():
    assert type(dish_volume_by_day(data_frame1)) == pd.Series, "It is the wrong data type"