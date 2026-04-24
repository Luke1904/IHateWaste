import re
from pathlib import Path

"""
Defines the path so it will work on any machine
"""
BASE_DIR = Path(__file__).parent.parent.parent

def excel_checker(x):
    if not re.search(r'\.xlsx$', str(x)):             # checks to see if the inserted file is an excel file
        raise ValueError("Need an excel")
    else:
        pass