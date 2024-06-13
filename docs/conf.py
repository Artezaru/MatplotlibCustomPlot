# Configuration file for the Sphinx documentation builder. 
# 
# For the full list of built-in configuration values, see the documentation: 
# https://www.sphinx-doc.org/en/master/usage/configuration.html 
 
# -- Project information ----------------------------------------------------- 
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information 
 
project = 'MatplotlibCustomPlot' 
copyright = ', Artezaru' 
author = 'Artezaru' 
release = 'version-0.0' 
 
 
import os 
import sphinx_rtd_theme 
import sys 
sys.path.insert(0, os.path.abspath('..')) 
 
# -- General configuration --------------------------------------------------- 
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration 
 
extensions = [ 
    'sphinx_rtd_theme', 
    'sphinx.ext.autodoc', 
    'sphinx_autodoc_typehints',  # Optional, for better type hint support 
] 
 
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store'] 
 
autodoc_default_options = { 
    'members': True, 
    'undoc-members': True, 
    'private-members': False, 
    'special-members': '__init__', 
    'inherited-members': True, 
    'show-inheritance': True 
} 
 
# -- Options for HTML output ------------------------------------------------- 
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output 
 
html_theme = 'sphinx_rtd_theme' 
html_static_path = ['_static'] 
html_output_path = 'docs' 
