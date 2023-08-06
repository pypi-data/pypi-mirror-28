#!/usr/bin/env python

from distutils.core import setup


setup(name='py3_lru_cache',
      version='0.1.6',
      description="""LRU cache for python. Provides a dictionary-like object as well as a method decorator. A fork of Chris Stucchio's py_lru_cache""",
      author='Alan Mock',
      author_email='pypi.org@alanmock.com',
      license='Dual: GPL v3 or BSD',
      url='https://github.com/amock/Python-LRU-cache',
      packages = ['lru'],
     )
