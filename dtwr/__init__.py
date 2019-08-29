# -*- coding: utf-8 -*-

"""Top-level package for Python port of R's Comprehensive Dynamic Time Warp algorithm package."""

__author__ = """Toni Giorgino"""
__email__ = 'toni.giorgino@gmail.com'
__version__ = '0.3.0'


from .dtw import *
from .stepPattern import *
from .data import *
from .countPaths import *
from .dtwPlot import *
from .mvm import *
from .warp import *
from .warpArea import *
from .window import *

import __main__ as main
if not hasattr(main, '__file__'):
    print("""Importing the dtwr module. When using in academic works please cite:
  T. Giorgino. Computing and Visualizing Dynamic Time Warping Alignments in R: The dtw Package.
  J. Stat. Soft., doi:10.18637/jss.v031.i07.\n""")


