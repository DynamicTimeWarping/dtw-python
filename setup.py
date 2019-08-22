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

requirements = [ 'numpy' ]

setup_requirements = [  ]

test_requirements = [ ]

ext=Extension('rdtw._dtw_utils',
              sources=['rdtw/dtw_computeCM.c','rdtw/_dtw_utils.pyx'],
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
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="Python port of R's Comprehensive Dynamic Time Warp algorithm package",
    entry_points={
        'console_scripts': [
            'rdtw=rdtw.cli:main',
        ],
    },
    install_requires=requirements,
    license="GNU General Public License v3",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='rdtw',
    name='rdtw',
#    packages=find_packages(include=['rdtw']),
    packages=['rdtw'],
    ext_modules=cythonize(ext),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/tonigi/rdtw',
    version='0.1.0',
    zip_safe=False,
)



