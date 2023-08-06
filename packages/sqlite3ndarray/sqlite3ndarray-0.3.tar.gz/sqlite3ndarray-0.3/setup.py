#!/usr/bin/env python
import hooks
from numpy.distutils.core import setup

VERSION = '0.3'

name = 'sqlite3ndarray'
long_description = open('README.rst').read()
keywords = 'database'
platforms = 'MacOS X,Linux,Solaris,Unix,Windows'

setup(name=name,
      version=hooks.get_version(name, VERSION),
      description='sqlite3 helpers for numpy ndarrays',
      long_description=long_description,
      url='http://pchanial.github.com/sqlite3ndarray',
      author='Pierre Chanial',
      author_email='pchanial@aneo.fr',
      maintainer='Pierre Chanial',
      maintainer_email='pchanial@aneo.fr',
      packages=['sqlite3ndarray'],
      platforms=platforms.split(','),
      keywords=keywords.split(','),
      cmdclass=hooks.cmdclass,
      classifiers=[
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.5',
          'Development Status :: 4 - Beta',
          'Intended Audience :: Science/Research',
          'Operating System :: OS Independent',
          'Topic :: Scientific/Engineering'])
