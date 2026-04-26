import re
from pathlib import Path

"""
Define the base directory of the project.

This allows file paths to be constructed in a way that works across
different machines and environments, instead of relying on hardcoded paths.
"""
BASE_DIR = Path(__file__).parent.parent.parent


def excel_checker(x):
    """
    Validate that the provided path corresponds to an Excel (.xlsx) file.

    Parameters
    ----------
    x : str or pathlib.Path
        Path to the file that needs to be checked.

    Raises
    ------
    ValueError
        If the file does not have a `.xlsx` extension.
    """

    # Convert input to string to ensure compatibility with regex
    # (in case a Path object is passed)
    if not re.search(r'\.xlsx$', str(x)):
        # Raise an error if the file is not an Excel file
        raise ValueError("Need an excel")