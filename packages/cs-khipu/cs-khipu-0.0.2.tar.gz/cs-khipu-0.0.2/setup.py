#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from setuptools import setup, find_packages

import os
import io

# Package meta-data.
NAME = 'cs-khipu'
DESCRIPTION = 'Unofficial Khipu Services Python SDK.'
URL = 'https://github.com/cornershop/python-khipu'
EMAIL = 'tech@cornershopapp.com'
AUTHOR = 'Cornershop'

# What packages are required for this module to be executed?
REQUIRED = [
    "requests", "arrow"
]

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.rst' is present in your MANIFEST.in file!
with io.open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = '\n' + f.read()

# Load the package's __version__.py module as a dictionary.
about = {}
with open(os.path.join(here, "khipu", '__about__.py')) as f:
    exec (f.read(), about)

setup(name=NAME,
      version=str(about['__version__']),
      description=DESCRIPTION,
      long_description=long_description,
      url=URL,
      author=AUTHOR,
      author_email=EMAIL,
      license='MIT',
      install_requires=REQUIRED,
      packages=find_packages(exclude=('tests',)),
      zip_safe=False)
