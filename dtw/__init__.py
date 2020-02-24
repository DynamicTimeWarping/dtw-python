# -*- coding: utf-8 -*-

"""Top-level package for the Comprehensive Dynamic Time Warp library.

Please see the help for the dtw.dtw() function which is the package's
main entry point.

"""

__author__ = """Toni Giorgino"""
__email__ = 'toni.giorgino@gmail.com'
__version__ = '1.0.5'

# There are no comments in this package because it mirrors closely the R sources.

from .dtw import *
from .stepPattern import *
from .countPaths import *
from .dtwPlot import *
from .mvm import *
from .warp import *
from .warpArea import *
from .window import *
from . import dtw_test_data


import __main__ as main
if not hasattr(main, '__file__'):
    print("""Importing the dtw module. When using in academic works please cite:
  T. Giorgino. Computing and Visualizing Dynamic Time Warping Alignments in R: The dtw Package.
  J. Stat. Soft., doi:10.18637/jss.v031.i07.\n""")


