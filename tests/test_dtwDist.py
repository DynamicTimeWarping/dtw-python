import unittest

import numpy as np
from numpy.testing import assert_allclose, assert_array_equal

from dtw import *


class TestDtwDist(unittest.TestCase):

    # Reference values from R: dtwDist(row(matrix(0, ncol=3, nrow=4)))
    def test_symmetric(self):
        m = np.tile(np.arange(1, 5), (3, 1)).T
        assert_array_equal(dtwDist(m), [[0, 5, 10, 15],
                                        [5, 0, 5, 10],
                                        [10, 5, 0, 5],
                                        [15, 10, 5, 0]])

    def test_definition(self):
        rng = np.random.default_rng(1)
        mx = rng.random((4, 5))
        my = rng.random((3, 6))
        dm = dtwDist(mx, my, step_pattern=asymmetric)
        self.assertEqual(dm.shape, (4, 3))
        for i in range(4):
            for j in range(3):
                self.assertEqual(dm[i, j],
                                 dtw(mx[i], my[j], step_pattern=asymmetric).distance)
        # Asymmetric pattern, asymmetric matrix
        ds = dtwDist(mx, step_pattern=asymmetric)
        self.assertFalse(np.allclose(ds, ds.T))

    def test_window_args(self):
        mx = np.random.default_rng(2).random((3, 10))
        assert_allclose(dtwDist(mx, window_type="sakoechiba", window_args={"window_size": 1}),
                        [[dtw(x, y, window_type="sakoechiba",
                              window_args={"window_size": 1}).distance for y in mx]
                         for x in mx])

    def test_lists_of_different_lengths(self):
        series = [np.arange(3), np.arange(5), np.arange(4)]
        dm = dtwDist(series)
        self.assertEqual(dm.shape, (3, 3))
        self.assertEqual(dm[0, 1], dtw(series[0], series[1]).distance)

    def test_single_series(self):
        self.assertEqual(dtwDist(np.arange(4)).shape, (1, 1))

    def test_errors(self):
        with self.assertRaises(ValueError):
            dtwDist(np.zeros((2, 3, 4)))
        with self.assertRaises(ValueError):
            dtwDist([np.zeros((2, 3))])


if __name__ == '__main__':
    unittest.main()
