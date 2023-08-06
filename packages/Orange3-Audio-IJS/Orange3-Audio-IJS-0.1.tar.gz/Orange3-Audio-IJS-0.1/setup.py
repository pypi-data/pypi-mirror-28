#!/usr/bin/env python

from os import path, walk

import sys
from setuptools import setup, find_packages

NAME = "Orange3-Audio-IJS"

VERSION = "0.1"

AUTHOR = "Department of Intelligent Systems | Jožef Stefan Institute - IJS"
AUTHOR_EMAIL = "info@ijs.si"

URL = "https://github.com/BuDnA/Audio-IJS"
DESCRIPTION = "Add-on for audio preprocessing and classification."
LONG_DESCRIPTION = open(path.join(path.dirname(__file__), 'README.md')).read()

LICENSE = "GSL3+"

CLASSIFIERS = [
    'Development Status :: 1 - Planning',
    'Intended Audience :: Education',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
    'Programming Language :: Python :: 3 :: Only'
]

KEYWORDS = (
    # [PyPi](https://pypi.python.org) packages with keyword "orange3 add-on"
    # can be installed using the Orange Add-on Manager
    'orange3 add-on',
    'orange3-audio-ijs'
)

PACKAGES = find_packages()

PACKAGE_DATA = {
    'orangecontrib.audio': ['tutorials/*.ows'],
    'orangecontrib.audio.widgets': ['icons/*'],
}

DATA_FILES = [
    # Data files that will be installed outside site-packages folder
]

INSTALL_REQUIRES = [
    'Orange3',
    'matplotlib',
    'liac-arff',
    'biosppy',
    'wavio',
    'six'
]

ENTRY_POINTS = {
    # Entry points that marks this package as an orange add-on. If set, addon will
    # be shown in the add-ons manager even if not published on PyPi.
    'orange3.addon': (
        'Audio - IJS = orangecontrib.audio',
    ),
    # Entry point used to specify packages containing tutorials accessible
    # from welcome screen. Tutorials are saved Orange Workflows (.ows files).
    'orange.widgets.tutorials': (
        # Syntax: any_text = path.to.package.containing.tutorials
        'exampletutorials = orangecontrib.audio.tutorials',
    ),

    # Entry point used to specify packages containing widgets.
    'orange.widgets': (
        # Syntax: category name = path.to.package.containing.widgets
        # Widget category specification can be seen in
        #    orangecontrib/example/widgets/__init__.py
        'Audio - IJS= orangecontrib.audio.widgets',
    ),

    # Register widget help
    "orange.canvas.help": (
        'html-index = orangecontrib.audio.widgets:WIDGET_HELP_PATH',)
}

NAMESPACE_PACKAGES = ["orangecontrib"]

TEST_SUITE = 'orangecontrib.audio.tests.suite'


def include_documentation(local_dir, install_dir):
    global DATA_FILES
    if 'bdist_wheel' in sys.argv and not path.exists(local_dir):
        print("Directory '{}' does not exist. "
              "Please build documentation before running bdist_wheel."
              .format(path.abspath(local_dir)))
        sys.exit(0)

    doc_files = []
    for dirpath, dirs, files in walk(local_dir):
        doc_files.append((dirpath.replace(local_dir, install_dir),
                          [path.join(dirpath, f) for f in files]))
    DATA_FILES.extend(doc_files)

if __name__ == '__main__':
    #include_documentation('doc/build/html', 'help/orange3-example')
    setup(
        name=NAME,
        version=VERSION,
	    author=AUTHOR,
        author_email=AUTHOR_EMAIL,
	    url=URL,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        license=LICENSE,
        packages=PACKAGES,
        package_data=PACKAGE_DATA,
        data_files=DATA_FILES,
        install_requires=INSTALL_REQUIRES,
        entry_points=ENTRY_POINTS,
        keywords=KEYWORDS,
	    classifiers=CLASSIFIERS,
        namespace_packages=NAMESPACE_PACKAGES,
        test_suite=TEST_SUITE
    )
