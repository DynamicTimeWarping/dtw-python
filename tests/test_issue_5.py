import unittest

import numpy as np
from numpy import nan
from numpy.testing import (assert_approx_equal, assert_equal,
                           assert_array_equal, assert_raises)
from dtw import *


def i(l):
    return np.array([int(x) for x in l.split()], dtype=int)-1



class TestIssues(unittest.TestCase):
    def test_issue_5(self):
        idx = np.linspace(0,6.28,num=100)
        query = np.sin(idx)

        idx1 = np.linspace(0,6.28,num=70)
        template = np.cos(idx1) + 0.5

        alignment = dtw(query, template,
                        step_pattern=rabinerJuangStepPattern(ptype=4,slope_weighting="c"),
                        keep_internals=True,open_end=False, open_begin=False)
        dist = alignment.distance
        test_index2 = alignment.index2

        assert_approx_equal(dist, 52.9795)

        ref_index2 = [0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8,
                      8, 9, 9, 10, 10, 11, 11, 12, 12, 13, 13, 14, 14,
                      15, 15, 16, 16, 17, 17, 18, 18, 19, 19, 20, 20,
                      21, 21, 22, 22, 23, 23, 24, 24, 25, 25, 26, 26,
                      27, 27, 28, 28, 29, 29, 30, 30, 31, 31, 32, 32,
                      33, 33, 34, 34, 35, 35, 36, 36, 37, 37, 38, 38,
                      39, 39, 40, 40, 41, 41, 42, 42, 43, 43, 45, 47,
                      49, 51, 53, 55, 57, 59, 61, 63, 65, 67, 69]

        assert_array_equal(test_index2, ref_index2)

        assert_equal(len(test_index2), 100)
