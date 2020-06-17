import unittest

import numpy as np
from numpy import nan
from numpy.testing import (assert_approx_equal, assert_equal,
                           assert_array_equal, assert_raises)
from dtw import *


def i(l):
    return np.array([int(x) for x in l.split()], dtype=int)-1


ldist = np.full((6, 6), 1.0)
ldist[1, :] = 0
ldist[:, 4] = 0
ldist[1, 4] = .01


"""Same tests as CRAN checks"""


class TestCRAN(unittest.TestCase):
    def test_ldist_symmetric2(self):
        ds = dtw(ldist, keep_internals=True)
        assert_equal(ds.distance, 2)
        assert_array_equal(ds.index1, i("1 2 2 2 3 4 5 6 6"))
        assert_array_equal(ds.index2, i("1 2 3 4 5 5 5 5 6"))
        assert_array_equal(ds.costMatrix, np.array(
            [[1,   2,   3,   4, 4.00, 5.00],
             [1,   1,   1,   1, 1.01, 1.01],
             [2,   2,   2,   2, 1.00, 2.00],
             [3,   3,   3,   3, 1.00, 2.00],
             [4,   4,   4,   4, 1.00, 2.00],
             [5,   5,   5,   5, 1.00, 2.00]], dtype=float))

    def test_ldist_asymmetric(self):
        ds = dtw(ldist, keep_internals=True, step_pattern=asymmetric)
        assert_equal(ds.distance, 2)
        assert_array_equal(ds.index1, np.arange(6))
        assert_array_equal(ds.index2, i("1 3 5 5 5 6"))

    def test_ldist_asymmetricP0(self):
        ds = dtw(ldist, keep_internals=True, step_pattern=asymmetricP0)
        assert_equal(ds.distance, 1)
        assert_array_equal(ds.index1, i("1 2 2 2 2 3 4 5 6 6"))
        assert_array_equal(ds.index2, i("1 1 2 3 4 5 5 5 5 6"))

    def test_ldist_asymmetricP1(self):
        ds = dtw(ldist, keep_internals=True, step_pattern=asymmetricP1)
        assert_equal(ds.distance, 3)
        assert_array_equal(ds.index1, i("1 2 3 3 4 5 6"))
        assert_array_equal(ds.index1s, i("1 2 3 5 6"))
        assert_array_equal(ds.index2, i("1 2 3 4 5 5 6"))
        assert_array_equal(ds.index2s, i("1 2 4 5 6"))

    # Count paths is in another file

    def test_open_begin_end(self):
        query = np.arange(2, 4)+.01
        ref = np.arange(4)+1
        obe = dtw(query, ref,
                  open_begin=True, open_end=True,
                  step_pattern=asymmetric)
        assert_approx_equal(obe.distance, 0.02)
        assert_array_equal(obe.index2, i("2 3"))

    def test_cdist(self):
        from scipy.spatial.distance import cdist

        query = np.vstack([np.arange(1, 11), np.ones(10)]).T
        ref = np.vstack([np.arange(11, 16), 2*np.ones(5)]).T

        cxdist = cdist(query, ref, metric="cityblock")

        d1 = dtw(query, ref, dist_method="cityblock").distance
        d2 = dtw(cxdist).distance

        assert_approx_equal(d1, d2)
