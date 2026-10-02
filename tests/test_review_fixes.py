import unittest

import numpy as np
from numpy.testing import assert_approx_equal, assert_array_equal
from dtw import *
from dtw.window import itakuraWindow


class TestReviewFixes(unittest.TestCase):
    def setUp(self):
        self.q, self.r = dtw_test_data.sin_cos()

    def test_warp_gaps_interpolated(self):
        w = warp(dtw([0, 2], [0, 1, 2], step_pattern="asymmetric"))
        assert_array_equal(w, [0, 0, 1])
        w = warp(dtw(self.q, self.r, step_pattern=asymmetric))
        self.assertTrue(np.all(w >= 0) and np.all(w < len(self.q)))

    def test_warp_open_begin_monotonic(self):
        a = dtw(self.q[40:80], self.r, step_pattern=asymmetric,
                open_begin=True, open_end=True)
        self.assertTrue(np.all(np.diff(warp(a)) >= 0))

    def test_warpArea_averages_ties(self):
        assert_approx_equal(warpArea(dtw([1, 2, 3, 4], [1, 2, 3, 4, 5, 6, 7, 8])), 6.0)

    def test_slantedband_reaches_corner(self):
        lm = np.random.default_rng(0).random((10, 100))
        dtw(lm, window_type="slantedband", window_args={"window_size": 5})

    def test_itakura_origin_and_corner(self):
        self.assertTrue(itakuraWindow(0, 0, 20, 30))
        self.assertTrue(itakuraWindow(19, 29, 20, 30))

    def test_open_begin_distance_only(self):
        kw = dict(step_pattern=asymmetric, open_begin=True, open_end=True)
        a = dtw(self.q[40:80], self.r, **kw)
        b = dtw(self.q[40:80], self.r, distance_only=True, **kw)
        assert_approx_equal(a.distance, b.distance)

    def test_unknown_names_raise_valueerror(self):
        with self.assertRaises(ValueError):
            dtw(self.q, self.r, window_type="nonexistent")
        with self.assertRaises(ValueError):
            rabinerJuangStepPattern(8)
        with self.assertRaises(ValueError):
            dtw(self.q, self.r, step_pattern="numpy")

    def test_window_abbreviation(self):
        a = dtw(self.q, self.r, window_type="sakoe", window_args={"window_size": 5})
        b = dtw(self.q, self.r, window_type="sakoechiba", window_args={"window_size": 5})
        assert_approx_equal(a.distance, b.distance)
