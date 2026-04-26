import os
import sys

sys.path.insert(0, os.path.abspath('../../src'))

project = 'Restaurant Inventory Analyzer'
author = 'Luca, Donovan & Sebastian'
release = '1.0.0'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.autosummary',
]

autosummary_generate = True
autodoc_member_order = 'bysource'

templates_path = ['_templates']
exclude_patterns = []

html_theme = 'sphinx_rtd_theme'

html_theme_options = {
    'navigation_depth': 4,
    'collapse_navigation': False,
    'sticky_navigation': True,
}

html_static_path = ['_static']

html_css_files = ['custom.css']