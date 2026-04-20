import re

if not re.search(r'\.xlsx$', path):
        raise ValueError("Need an excel")