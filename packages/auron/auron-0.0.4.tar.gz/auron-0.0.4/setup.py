from __future__ import print_function

import os
import sys

from pprint import pprint
from termcolor import colored
from setuptools import setup, find_packages
from auron import __version__

sys.dont_write_bytecode = True

setup(
    name="auron",
    version=__version__,
    author="Ruben van Staden",
    author_email="rubenvanstaden@gmail.com",
    description="",
    setup_requires=['setuptools-markdown'],
    long_description_markdown_filename='README.md',
    license="BSD",
    keywords="auron",
    url="https://github.com/rubenvanstaden/auron",
    packages=['auron', 'tests'],
    package_dir={'auron': 'auron'},
    install_requires=[
        'gdsyuna', 
        'yuna',
        'networkx'
    ]
)
