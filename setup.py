#!/usr/bin/env python3

from os import path, walk

from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    ABOUT = f.read()

NAME = 'Orange3-Sqlite3'

MAJOR = 0
MINOR = 0
MICRO = 3
VERSION = '%d.%d.%d' % (MAJOR, MINOR, MICRO)

AUTHOR = 'Chris Lee'
AUTHOR_EMAIL = 'github@chrislee.dhs.org'

URL = 'https://github.com/chrislee35/orange3-sqlite3'
DESCRIPTION = 'Simple widget to load a table from an SQL query against an SQLite3 database'
LONG_DESCRIPTION = ABOUT
LICENSE = 'GPL3+'

CLASSIFIERS = [
    'Development Status :: 1 - Planning',
    'Intended Audience :: Education',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
    'Programming Language :: Python :: 3 :: Only'
]

KEYWORDS = [
    'orange3 add-on',
]

PACKAGES = find_packages()

PACKAGE_DATA = {
    'orangecontrib.sqlite3.widgets': ['icons/*.svg'],
}

ENTRY_POINTS = {
    'orange.widgets':
        ('Sqlite3 = orangecontrib.sqlite3.widgets',),
    'orange3.addon':
        ('Orange3-Sqlite3 = orangecontrib.sqlite3',),
    # Register widget help
    "orange.canvas.help": (
        'html-index = orangecontrib.sqlite3.widgets:WIDGET_HELP_PATH',)
}

DATA_FILES = [
    # Data files that will be installed outside site-packages folder
]


def include_documentation(local_dir, install_dir):
    global DATA_FILES
    # if 'bdist_wheel' in sys.argv and not path.exists(local_dir):
    #     print("Directory '{}' does not exist. "
    #           "Please build documentation before running bdist_wheel."
    #           .format(path.abspath(local_dir)))
    #     sys.exit(0)
    doc_files = []
    for dirpath, dirs, files in walk(local_dir):
        doc_files.append((dirpath.replace(local_dir, install_dir),
                          [path.join(dirpath, f) for f in files]))
    DATA_FILES.extend(doc_files)


if __name__ == '__main__':
    include_documentation('doc/_build/html', 'help/orange3-sqlite3')
    setup(
        name=NAME,
        version=VERSION,
        author=AUTHOR,
        author_email=AUTHOR_EMAIL,
        url=URL,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        long_description_content_type='text/markdown',
        license=LICENSE,
        packages=PACKAGES,
        data_files=DATA_FILES,
        package_data=PACKAGE_DATA,
        keywords=KEYWORDS,
        classifiers=CLASSIFIERS,
        install_requires=[
            "AnyQt",
            "numpy >=1.26",
            "Orange3 >=3.34.0",
            "orange-canvas-core >=0.1.28",
            "orange-widget-base >=4.20.0"
        ],
        extras_require={
            'test': ['coverage', ],
            'doc': ['sphinx', 'recommonmark', 'sphinx_rtd_theme', ],
        },
        namespace_packages=['orangecontrib'],
        entry_points=ENTRY_POINTS,
    )