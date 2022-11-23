# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
import os
import sys

from parble import __version__

sys.path.insert(0, os.path.abspath(".."))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Parble-python"
copyright = "2022, Smart and Easy NV"
author = "ParbleLabs"
release = __version__

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["sphinx.ext.napoleon", "sphinx.ext.autodoc", "sphinx_click"]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# html_theme = "sphinx_book_theme"
html_theme = "pydata_sphinx_theme"
html_static_path = ["_static"]
html_logo = "parble-logo.png"
html_favicon = "parble-icon.png"
html_title = "Parble Python SDK"
html_theme_options = {
    "logo": {"text": html_title, "alt_text": "Parble Logo"},
    "github_url": "https://github.com/parblelabs/parble-python",
    "twitter_url": "https://twitter.com/parblelabs",
    "footer_items": ["copyright", "sphinx-version"],
}
html_css_files = [
    "custom.css",
]

autodoc_typehints = "description"
autodoc_class_signature = "separated"
