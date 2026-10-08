#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script. Project metadata lives in pyproject.toml."""

from setuptools import setup, Extension

# setuptools runs Cython on the .pyx source (Cython is a build requirement).
setup(
    ext_modules=[
        Extension("dtw._dtw_utils", sources=["dtw/_dtw_utils.pyx", "dtw/dtw_core.c"])
    ],
)
