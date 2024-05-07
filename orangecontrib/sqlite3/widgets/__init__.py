"""
Sqlite3 Widget
===============

Widgets for querying Sqlite3
"""
import sysconfig

NAME = "Sqlite3"
DESCRIPTION = "Sqlite3 Widgets"

ICON = "icons/sqlite3.svg"
PRIORITY = 1000
BACKGROUND = "#ffe640"

WIDGET_HELP_PATH = (
# Used for development.
# You still need to build help pages using
# make html
# inside doc folder
("{DEVELOP_ROOT}/doc/_build/html/index.html", None),

# Documentation included in wheel
# Correct DATA_FILES entry is needed in setup.py and documentation has to be
# built before the wheel is created.
("{}/help/orange3-sqlite3/index.html".format(sysconfig.get_path("data")),
 None),

# Online documentation url, used when the local documentation is available.
# Url should point to a page with a section Widgets. This section should
# includes links to documentation pages of each widget. Matching is
# performed by comparing link caption to widget name.
("http://orange3-sqlite3.readthedocs.io/en/latest/", "")
)