#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages
from setuptools.extension import Extension
from setuptools import dist

# Numpy is required even to build source ----------
dist.Distribution().fetch_build_eggs(['numpy>=1.14'])
import numpy                    # autopep8 breaks this!


# Cython is optional ----------
have_cython = False
try:
    from Cython.Build import cythonize
    import Cython

    ext = [Extension('dtw._dtw_utils',
                 sources=['dtw/_dtw_utils.pyx', 'dtw/dtw_computeCM.c'],
                 include_dirs=[numpy.get_include()])]
    ext = cythonize(ext)
    cmdclass={'build_cython': Cython.Build.build_ext}
    have_cython = True
except:
    ext = [Extension('dtw._dtw_utils',
                 sources=['dtw/_dtw_utils.c', 'dtw/dtw_computeCM.c'],
                 include_dirs=[numpy.get_include()])]
    cmdclass = {}


# --------------------    
with open('README.rst') as readme_file:
    readme_rst = readme_file.read()


setup(
    author="Toni Giorgino",
    author_email='toni.giorgino@gmail.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
        'License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="A comprehensive implementation of dynamic time warping (DTW) algorithms. DTW computes the optimal (least cumulative distance) alignment between points of two time series. Common DTW variants covered include local (slope) and global (window) constraints, subsequence matches, arbitrary distance definitions, normalizations, minimum variance matching, and so on. Provides cumulative distances, alignments, specialized plot styles, etc.",
    entry_points={
        'console_scripts': [
            'dtw=dtw.__main__:main',
        ],
    },
    install_requires=['numpy>=1.12', 'scipy>=1.1'],
    # setup_requires=['cython', 'numpy'],  # In principle deprecated for toml, but actually used by sdist
    tests_require=["pytest"],                 # Obsolete
    python_requires='>=3.6',
    license="GNU General Public License v3",
    long_description=readme_rst,
    long_description_content_type="text/x-rst",
    include_package_data=True,
    keywords=['dtw', 'timeseries'],
    name='dtw-python',
    #    packages=find_packages(include=['dtw']),
    packages=['dtw'],
    package_data={'dtw': ['data/*.csv']},
    ext_modules=ext,
    cmdclass=cmdclass,
    url='https://DynamicTimeWarping.github.io',
    version='1.1.5',
    zip_safe=False,
)
