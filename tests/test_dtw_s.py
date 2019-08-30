import unittest

import numpy as np
from numpy import nan
from numpy.testing import (assert_approx_equal,
                           assert_array_equal, assert_raises)
from dtw import *

        
class TestDTWs(unittest.TestCase):
    def test_matrix(self):
        dm = 10 * np.ones((4, 4)) + np.eye(4)
        al = dtw(dm, keep_internals=True)
        assert_array_equal(al.costMatrix,
                           np.array([[11., 21., 31., 41.],
                                     [21., 32., 41., 51.],
                                     [31., 41., 52., 61.],
                                     [41., 51., 61., 72.]]))

    def test_rectangular(self):
        # Hand-checked
        x = np.array([1, 2, 3])
        y = np.array([2, 3, 4, 5, 6])
        al = dtw(x, y, keep_internals=True)
        assert_array_equal(al.costMatrix,
                           np.array([[1., 3., 6., 10., 15.],
                                     [1., 2., 4., 7., 11.],
                                     [2., 1., 2., 4., 7.]]))
        assert_approx_equal(al.normalizedDistance,0.875)
        

    def test_backtrack(self):
        x = np.array([1, 2, 3])
        y = np.array([2, 3, 4, 5, 6])
        al = dtw(x, y)
        assert_array_equal(al.index1,  np.array([0, 1, 2, 2, 2, 2]))
        assert_array_equal(al.index1s, np.array([0, 1, 2, 2, 2, 2]))
        assert_array_equal(al.index2,  np.array([0, 0, 1, 2, 3, 4]))
        assert_array_equal(al.index2s, np.array([0, 0, 1, 2, 3, 4]))
        

    def test_vectors(self):
        x = np.array([1, 2, 3])
        y = np.array([2, 3, 4])
        al = dtw(x, y)
        assert_approx_equal(al.distance, 2.0)

    def test_asymmetric(self):
        lm = np.array([[1, 1, 2, 2, 3, 3],
                       [1, 1, 1, 2, 2, 2],
                       [3, 1, 2, 2, 3, 3],
                       [3, 1, 2, 1, 1, 2],
                       [3, 2, 1, 2, 1, 2],
                       [3, 3, 3, 2, 1, 2]], dtype=np.double)
        alignment = dtw(lm, step_pattern=asymmetric, keep_internals=True)
        assert_array_equal(alignment.costMatrix,
                           np.array([[1., nan, nan, nan, nan, nan],
                                     [2., 2., 2., nan, nan, nan],
                                     [5., 3., 4., 4., 5., nan],
                                     [8., 4., 5., 4., 5., 6.],
                                     [11., 6., 5., 6., 5., 6.],
                                     [14., 9., 8., 7., 6., 7.]])
                           )

    def test_impossible(self):
        x = np.ones(4)
        y = np.ones(20)
        with assert_raises(ValueError):
            dtw(x, y, step_pattern=asymmetric)

        
