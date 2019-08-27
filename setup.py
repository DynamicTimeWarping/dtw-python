#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages
from setuptools.extension import Extension
from Cython.Build import cythonize
#from numpy.distutils.misc_util import Configuration
import numpy

    
with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

# requirements = ['Click>=6.0', ]

requirements = [ 'numpy', 'scipy' ]

setup_requirements = [ ]

test_requirements = [ ]

ext=Extension('dtwr._dtw_utils',
              sources=['dtwr/dtw_computeCM.c','dtwr/_dtw_utils.pyx'],
              include_dirs=[numpy.get_include()]
)


setup(
    author="Toni Giorgino",
    author_email='toni.giorgino@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="A comprehensive implementation of dynamic time warping (DTW) algorithms in R. DTW computes the optimal (least cumulative distance) alignment between points of two time series. Common DTW variants covered include local (slope) and global (window) constraints, subsequence matches, arbitrary distance definitions, normalizations, minimum variance matching, and so on. Provides cumulative distances, alignments, specialized plot styles, etc.",
    entry_points={
        'console_scripts': [
            'dtwr=dtwr.cli:main',
        ],
    },
    install_requires=requirements,
    license="GNU General Public License v3",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='dtwr',
    name='dtwr',
#    packages=find_packages(include=['dtwr']),
    packages=['dtwr'],
    package_data={'dtwr': ['data/*.csv']},
    ext_modules=cythonize(ext),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/tonigi/dtwr-py',
    version='0.1.1',
    zip_safe=False,
)



