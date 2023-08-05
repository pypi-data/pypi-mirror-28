#!/usr/bin/env python

#from distutils.core import setup
from setuptools import setup
import os
import sys

if sys.version_info < (3, 6):
    sys.exit('Sorry, Python < 3.6 is not supported.')
# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

with open('Monopoly/__init__.py', 'rb') as fid:
    for line in fid:
        line = line.decode('utf-8')
        if line.startswith('__version__'):
            version = line.strip().split()[-1][1:-1]
            break

download_url = ('https://github.com/rjslater2000/Monopoly/\
                blob/master/dist/Monopoly-' + version + '.whl')
#https://github.com/rjslater2000/RyGames/archive/0.1a1.zip

setup(name='Monopopy',
      version=version,
      description=('Monopoly clone using PyGame by Ryan J. Slater'),
      author=u'Ryan J. Slater',
      author_email='ryan.j.slater.2@gmail.com',
      url='https://github.com/rjslater2000/Monopoly',
      packages=['Monopoly'],
      package_data={'Monopoly': ['../README.md', 'data/*.mat'],
                        '': ['README.md']},
      long_description=read('README.md'),
      keywords=['Monopoly'],
      install_requires=['pygame'],
      )

# https://docs.python.org/3/distutils/setupscript.html#additional-meta-data
