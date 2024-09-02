#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup
from setuptools.extension import Extension
from Cython.Build import cythonize
import numpy


setup(
    include_package_data=True,
    name="dtw-python",
    #    packages=find_packages(include=['dtw']),
    packages=["dtw"],
    include_dirs=numpy.get_include(),
    ext_modules=cythonize(
        [Extension("dtw._dtw_utils", sources=["dtw/_dtw_utils.pyx", "dtw/dtw_core.c"])],
        force=True,
    ),
    url="https://DynamicTimeWarping.github.io",
    version="1.5.3",
    zip_safe=False,
)
