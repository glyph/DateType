# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import pathlib
import subprocess

_project_root = pathlib.Path(__file__).parent.parent
_source_root = _project_root / "src"

project = 'DateType'
copyright = '2025, Glyph'
author = 'Glyph'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

_git_reference = subprocess.run(
    ["git", "rev-parse", "--abbrev-ref", "HEAD"],
    text=True,
    encoding="utf8",
    capture_output=True,
    check=True,
).stdout
extensions = [
    "sphinx.ext.intersphinx",
    "pydoctor.sphinx_ext.build_apidocs",
]
pydoctor_args = [
    # pydoctor should not fail the sphinx build, we have another tox environment for that.
    "--intersphinx=https://docs.python.org/3/objects.inv",
    f"--config={_project_root}/.pydoctor.cfg",
    f"--html-viewsource-base=https://github.com/glyph/datetype/tree/{_git_reference}/src",
    f"--project-base-dir={_source_root}",
    "--html-output={outdir}/api",
    "--privacy=HIDDEN:datetype.test.*",
    "--privacy=HIDDEN:datetype.test",
    "--privacy=HIDDEN:**.__post_init__",
    str(_source_root / "datetype"),
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

intersphinx_mapping = {
    "py3": ("https://docs.python.org/3", None),
}

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
