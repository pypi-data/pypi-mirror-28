# -*- coding: utf-8 -*-
"""
This module contains the tool of birdhousebuilder.recipe.sphinx
"""
import os
from setuptools import setup, find_packages


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()


name = 'birdhousebuilder.recipe.sphinx'

version = '0.2.4'
description = "Buildout recipe to generate and Sphinx-based documentation for Birdhouse."
long_description = (
    read('README.rst') + '\n' +
    read('AUTHORS.rst') + '\n' +
    read('CHANGES.rst')
)

entry_points = '''
[zc.buildout]
default = %(name)s:Recipe
[zc.buildout.uninstall]
default = %(name)s:uninstall
''' % globals()

reqs = ['setuptools',
        'zc.buildout',
        # -*- Extra requirements: -*-
        'mako',
        'zc.recipe.egg',
        'birdhousebuilder.recipe.conda',
        ],
tests_reqs = ['zope.testing', 'zc.buildout']

setup(name=name,
      version=version,
      description=description,
      long_description=long_description,
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
          'Framework :: Buildout',
          'Intended Audience :: Developers',
          'Programming Language :: Python :: 2',
          'Topic :: Software Development :: Build Tools',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: Scientific/Engineering :: Atmospheric Science',
      ],
      keywords='buildout sphinx birdhouse',
      author='Birdhouse',
      author_email='wps-dev@dkrz.de',
      url='https://github.com/birdhouse/birdhousebuilder.recipe.sphinx',
      license='Apache License 2.0',
      install_requires=reqs,
      extras_require=dict(tests=tests_reqs),
      entry_points=entry_points,
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['birdhousebuilder', 'birdhousebuilder.recipe'],
      include_package_data=True,
      zip_safe=False,
      )
