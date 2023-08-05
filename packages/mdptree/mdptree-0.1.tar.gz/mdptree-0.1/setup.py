#!/usr/bin/env python
import hooks
from numpy.distutils.core import setup

VERSION = '0.1'

name = 'mdptree'
long_description = open('README.rst').read()
keywords = 'statistics'
platforms = 'MacOS X,Linux,Solaris,Unix,Windows'

setup(name=name,
      version=hooks.get_version(name, VERSION),
      description='Tools to model Markov Decision Processes',
      long_description=long_description,
      url='http://pchanial.github.com/mdptree',
      author='Pierre Chanial',
      author_email='pchanial@aneo.fr',
      maintainer='Pierre Chanial',
      maintainer_email='pchanial@aneo.fr',
      packages=['mdptree'],
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
