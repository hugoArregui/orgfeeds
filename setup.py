#!/usr/bin/env python

from distutils.core import setup

setup(name='orgfeeds',
      version='0.1',
      description='org mode feeds!',
      author='Hugo Arregui',
      packages=['orgfeeds'],
      scripts=['bin/refresh.py'])
