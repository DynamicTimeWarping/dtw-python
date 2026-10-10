import unittest

import numpy as np
import scipy.stats
from numpy.testing import assert_allclose

from dtw import *
from dtw.permutationTest import _permute_derivative

QUERY = np.array([0, 2, 1, 4, 3, 5], dtype=float)
REFERENCE = np.array([1, 0, 3, 2, 5, 4], dtype=float)
STATISTICS = ["distance", "normalizedDistance", "pearson", "spearman", "kendall"]


def correlation(x, y, method):
    if method == "pearson":
        return np.corrcoef(x, y)[0, 1]
    elif method == "spearman":
        return scipy.stats.spearmanr(x, y)[0]
    return scipy.stats.kendalltau(x, y)[0]


# An independent reference calculation aligns the actual permuted series,
# drawing the permutations in the same order as permutationTest()
def shuffle(x, what, rng):
    x = np.atleast_2d(np.asarray(x, dtype=float).T).T
    if what == "values":
        return x[rng.permutation(x.shape[0]), :]
    if x.shape[0] == 1:
        return x
    increments = np.diff(x, axis=0)
    increments = increments[rng.permutation(increments.shape[0]), :]
    return np.cumsum(np.vstack([x[:1, :], increments]), axis=0)


def manual(q, r, what, side, statistic, seed, R=9, **kwargs):
    rng = np.random.default_rng(seed)
    out = []
    for i in range(R):
        x = shuffle(q, what, rng) if side in ("query", "both") else np.atleast_2d(q.T).T
        y = shuffle(r, what, rng) if side in ("reference", "both") else np.atleast_2d(r.T).T
        a = dtw(x, y, keep_internals=True, **kwargs)
        if statistic in ("distance", "normalizedDistance"):
            out.append(getattr(a, statistic))
        else:
            out.append(correlation(x[a.index1, 0], y[a.index2, 0], statistic))
    return np.array(out)


def distribution(alignment, seed, **kwargs):
    return permutationTest(alignment, rng=seed, return_distribution=True,
                           **kwargs).null_distribution


class TestPermutationTest(unittest.TestCase):

    def setUp(self):
        self.alignment = dtw(QUERY, REFERENCE, keep_internals=True)

    # Every statistic, null, and side must agree with realignment of shuffled data.
    def test_against_manual_realignment(self):
        a = self.alignment
        for what in ["values", "increments"]:
            for side in ["query", "reference", "both"]:
                for statistic in STATISTICS:
                    with self.subTest(what=what, side=side, statistic=statistic):
                        expected = manual(QUERY, REFERENCE, what, side, statistic, 982)
                        actual = distribution(a, 982, R=9, permute_what=what,
                                              permute_side=side, statistic=statistic)
                        assert_allclose(actual, expected, rtol=1e-12)
                        if statistic in ("distance", "normalizedDistance"):
                            observed = getattr(a, statistic)
                        else:
                            observed = correlation(QUERY[a.index1], REFERENCE[a.index2],
                                                   statistic)
                        tolerance = 100 * np.finfo(float).eps * max(1, abs(observed))
                        lower = (1 + np.sum(expected <= observed + tolerance)) / 10
                        upper = (1 + np.sum(expected >= observed - tolerance)) / 10
                        for alternative, p in [("less", lower), ("greater", upper),
                                               ("two-sided", min(1, 2 * min(lower, upper)))]:
                            result = permutationTest(a, R=9, permute_what=what,
                                                     permute_side=side, statistic=statistic,
                                                     alternative=alternative, rng=982)
                            self.assertAlmostEqual(result.p_value, p, places=12)
                            self.assertAlmostEqual(result.estimate, observed, places=12)
                            self.assertEqual(result.replicates, 9)
                            self.assertEqual(result.alternative, alternative)
                            self.assertEqual(result.statistic, statistic)
                            self.assertGreater(result.p_value, 0)
                            self.assertIsNone(result.null_distribution)

    def test_default_alternative(self):
        self.assertEqual(permutationTest(self.alignment, R=1).alternative, "less")
        self.assertEqual(permutationTest(self.alignment, R=1, statistic="pearson").alternative,
                         "greater")

    # Retaining the draws preserves the test result and its printed summary.
    def test_return_distribution(self):
        summary = permutationTest(self.alignment, R=9, rng=21)
        retained = permutationTest(self.alignment, R=9, rng=21, return_distribution=True)
        self.assertEqual(retained.null_distribution.shape, (9,))
        self.assertEqual(retained.p_value, summary.p_value)
        self.assertEqual(retained.estimate, summary.estimate)
        self.assertEqual(repr(retained), repr(summary))
        self.assertIn("p-value", repr(summary))

    def test_rng_reproducible(self):
        gen = np.random.default_rng(7)
        d1 = distribution(self.alignment, gen, R=20)
        d2 = distribution(self.alignment, np.random.default_rng(7), R=20)
        assert_allclose(d1, d2)

    # All ties must give p=1, including reconstructed floating-point increments.
    def test_ties(self):
        for q in [np.ones(6), np.arange(1, 7), np.linspace(0, 1, 6)]:
            a = dtw(q, q, keep_internals=True)
            for alternative in ["less", "greater", "two-sided"]:
                self.assertEqual(permutationTest(a, R=19, permute_what="increments",
                                                 alternative=alternative, rng=1).p_value, 1)
        constant = dtw(np.ones(6), np.ones(6), keep_internals=True)
        self.assertEqual(permutationTest(constant, R=19, permute_what="values",
                                         rng=1).p_value, 1)

    # The observed identity alignment is the strict minimum in this sampled set.
    def test_identity_minimum(self):
        a = dtw(np.arange(1, 7), np.arange(1, 7), keep_internals=True)
        draws = distribution(a, 10, R=19, permute_what="values")
        self.assertTrue(np.all(draws > 0))
        self.assertAlmostEqual(permutationTest(a, R=19, permute_what="values",
                                               rng=10).p_value, 1 / 20)

    # Window arguments, including custom windows, are reused.
    def test_windows(self):
        def band(iw, jw, query_size, reference_size, width=100):
            return abs(iw - jw) <= width

        windowed = dtw(QUERY, REFERENCE, window_type=band, window_args={"width": 0},
                       keep_internals=True)
        for what in ["values", "increments"]:
            with self.subTest(what=what):
                expected = manual(QUERY, REFERENCE, what, "both", "distance", 53,
                                  window_type=band, window_args={"width": 0})
                assert_allclose(distribution(windowed, 53, R=9, permute_what=what,
                                             permute_side="both"), expected)
                for window in ["sakoechiba", "slantedband"]:
                    a = dtw(QUERY, REFERENCE, window_type=window,
                            window_args={"window_size": 1}, keep_internals=True)
                    expected = manual(QUERY, REFERENCE, what, "query", "distance", 53,
                                      window_type=window, window_args={"window_size": 1})
                    assert_allclose(distribution(a, 53, R=9, permute_what=what), expected)

    # Open begin/end and normalization must also be carried through.
    def test_open_begin_end(self):
        kw = dict(step_pattern=asymmetric, open_begin=True, open_end=True)
        a = dtw(QUERY, REFERENCE, keep_internals=True, **kw)
        for what in ["values", "increments"]:
            with self.subTest(what=what):
                expected = manual(QUERY, REFERENCE, what, "query", "normalizedDistance", 83, **kw)
                assert_allclose(distribution(a, 83, R=9, permute_what=what,
                                             statistic="normalizedDistance"), expected)

    # Multivariate increments stay together and reuse the original distance method.
    def test_multivariate(self):
        q = np.column_stack([QUERY, REFERENCE])
        r = np.column_stack([REFERENCE, 2 * QUERY])
        a = dtw(q, r, dist_method="cityblock", keep_internals=True)
        for what in ["values", "increments"]:
            with self.subTest(what=what):
                expected = manual(q, r, what, "both", "distance", 61, dist_method="cityblock")
                assert_allclose(distribution(a, 61, R=9, permute_what=what,
                                             permute_side="both"), expected)
        shuffled = _permute_derivative(q, np.random.default_rng(1))
        assert_allclose(shuffled[[0, -1], :], q[[0, -1], :])
        self.assertEqual(shuffled.shape, q.shape)
        with self.assertRaisesRegex(ValueError, "univariate"):
            permutationTest(a, R=1, statistic="pearson")

    # Precomputed cost matrices support value tests without access to raw series.
    def test_precomputed_cost_matrix(self):
        a = dtw(self.alignment.localCostMatrix, keep_internals=True)
        assert_allclose(distribution(a, 1, R=9, permute_what="values"),
                        distribution(self.alignment, 1, R=9, permute_what="values"))
        with self.assertRaisesRegex(ValueError, "original query and reference"):
            permutationTest(a, R=1, permute_what="increments")
        with self.assertRaisesRegex(ValueError, "original query and reference"):
            permutationTest(a, R=1, permute_what="values", statistic="pearson")

    # A distance-only input has its path recomputed for correlations.
    def test_distance_only(self):
        a = dtw(QUERY, REFERENCE, keep_internals=True, distance_only=True)
        r1 = permutationTest(a, R=9, statistic="spearman", rng=4)
        r2 = permutationTest(self.alignment, R=9, statistic="spearman", rng=4)
        self.assertEqual(r1.estimate, r2.estimate)
        self.assertEqual(r1.p_value, r2.p_value)

    # A series of length one can be used for distance statistics.
    def test_singleton(self):
        a = dtw([1.0], REFERENCE, keep_internals=True)
        self.assertEqual(permutationTest(a, R=5, permute_what="increments").p_value, 1)
        _permute_derivative(np.ones((1, 2)), np.random.default_rng(1))

    def test_errors(self):
        a = self.alignment
        with self.assertRaisesRegex(ValueError, "keep_internals"):
            permutationTest(dtw(QUERY, REFERENCE), R=1)
        with self.assertRaises(TypeError):
            permutationTest("not an alignment", R=1)
        for bad in [0, -1, 1.5, np.inf, np.nan, "10", True]:
            with self.assertRaisesRegex(ValueError, "R must be"):
                permutationTest(a, R=bad)
        with self.assertRaisesRegex(ValueError, "return_distribution"):
            permutationTest(a, R=1, return_distribution="yes")
        with self.assertRaisesRegex(ValueError, "alternative"):
            permutationTest(a, R=1, alternative="two.sided")
        with self.assertRaisesRegex(ValueError, "permute_side"):
            permutationTest(a, R=1, permute_side="left")
        with self.assertRaisesRegex(ValueError, "permute_what"):
            permutationTest(a, R=1, permute_what="blocks")
        with self.assertRaisesRegex(ValueError, "statistic"):
            permutationTest(a, R=1, statistic="cosine")
        with self.assertRaisesRegex(ValueError, "normalizable"):
            permutationTest(dtw(QUERY, REFERENCE, step_pattern=symmetric1,
                                keep_internals=True), R=1, statistic="normalizedDistance")
        with self.assertRaisesRegex(ValueError, "undefined"):
            permutationTest(dtw(np.ones(6), REFERENCE, keep_internals=True), R=1,
                            statistic="pearson")


if __name__ == '__main__':
    unittest.main()
