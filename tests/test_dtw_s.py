import unittest

import numpy as np
from numpy import nan
from numpy.testing import assert_approx_equal, assert_array_equal, assert_raises
from dtw import *


class TestDTWs(unittest.TestCase):
    def test_matrix(self):
        dm = 10 * np.ones((4, 4)) + np.eye(4)
        al = dtw(dm, keep_internals=True)
        assert_array_equal(
            al.costMatrix,
            np.array(
                [
                    [11.0, 21.0, 31.0, 41.0],
                    [21.0, 32.0, 41.0, 51.0],
                    [31.0, 41.0, 52.0, 61.0],
                    [41.0, 51.0, 61.0, 72.0],
                ]
            ),
        )

    def test_rectangular(self):
        # Hand-checked
        x = np.array([1, 2, 3])
        y = np.array([2, 3, 4, 5, 6])
        al = dtw(x, y, keep_internals=True)
        assert_array_equal(
            al.costMatrix,
            np.array(
                [
                    [1.0, 3.0, 6.0, 10.0, 15.0],
                    [1.0, 2.0, 4.0, 7.0, 11.0],
                    [2.0, 1.0, 2.0, 4.0, 7.0],
                ]
            ),
        )
        assert_approx_equal(al.normalizedDistance, 0.875)

    def test_backtrack(self):
        x = np.array([1, 2, 3])
        y = np.array([2, 3, 4, 5, 6])
        al = dtw(x, y)
        assert_array_equal(al.index1, np.array([0, 1, 2, 2, 2, 2]))
        assert_array_equal(al.index1s, np.array([0, 1, 2, 2, 2, 2]))
        assert_array_equal(al.index2, np.array([0, 0, 1, 2, 3, 4]))
        assert_array_equal(al.index2s, np.array([0, 0, 1, 2, 3, 4]))

    def test_vectors(self):
        x = np.array([1, 2, 3])
        y = np.array([2, 3, 4])
        al = dtw(x, y)
        assert_approx_equal(al.distance, 2.0)

    def test_asymmetric(self):
        lm = np.array(
            [
                [1, 1, 2, 2, 3, 3],
                [1, 1, 1, 2, 2, 2],
                [3, 1, 2, 2, 3, 3],
                [3, 1, 2, 1, 1, 2],
                [3, 2, 1, 2, 1, 2],
                [3, 3, 3, 2, 1, 2],
            ],
            dtype=np.double,
        )
        alignment = dtw(lm, step_pattern=asymmetric, keep_internals=True)
        assert_array_equal(
            alignment.costMatrix,
            np.array(
                [
                    [1.0, nan, nan, nan, nan, nan],
                    [2.0, 2.0, 2.0, nan, nan, nan],
                    [5.0, 3.0, 4.0, 4.0, 5.0, nan],
                    [8.0, 4.0, 5.0, 4.0, 5.0, 6.0],
                    [11.0, 6.0, 5.0, 6.0, 5.0, 6.0],
                    [14.0, 9.0, 8.0, 7.0, 6.0, 7.0],
                ]
            ),
        )

    def test_impossible(self):
        x = np.ones(4)
        y = np.ones(20)
        with assert_raises(ValueError):
            dtw(x, y, step_pattern=asymmetric)
