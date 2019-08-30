
import unittest

import numpy as np
from numpy import nan
from numpy.testing import *

from dtw import *
from dtw.countPaths import *


class Test_countPaths(unittest.TestCase):

    # From dtw()'s example
    def test_example_ds(self):
        ldist = np.full( (6,6), 1.0)
        ldist[1,:] = 0
        ldist[:,4] = 0
        ldist[1,4] = .01
        ds = dtw(ldist, keep_internals=True)
        pds = countPaths(ds)
        assert_equal(pds, 1683)
        
    def test_example_da(self):
        ldist = np.full( (6,6), 1.0)
        ldist[1,:] = 0
        ldist[:,4] = 0
        ldist[1,4] = .01

        da = dtw(ldist, step_pattern=asymmetric, keep_internals=True)
        pda = countPaths(da)
        assert_equal(pda, 51)        
        
