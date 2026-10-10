import unittest

import numpy as np
from numpy.testing import assert_array_equal

from dtw import *

FIELDS = ["index1", "index2", "index1s", "index2s", "stepsTaken"]


# An independent reference: enumerate every path forward from [0,0]
def allPaths(a):
    lm = a.localCostMatrix
    N, M = lm.shape
    sp = a.stepPattern.mx
    ix, jx = np.indices((N, M))
    wm = np.broadcast_to(a.windowFunction(ix, jx, query_size=N, reference_size=M,
                                          **a.windowArgs), (N, M))
    out = []

    def visit(i, j, cost, i1, i2, i1s, i2s, st):
        if i == N - 1 and (j == M - 1 or a.openEnd):
            out.append(dict(index1=i1, index2=i2, index1s=i1s, index2s=i2s,
                            stepsTaken=st, distance=cost))
        for k in range(1, a.stepPattern.get_n_patterns() + 1):
            p = sp[sp[:, 0] == k, 1:]
            I, J = i + int(p[0, 0]), j + int(p[0, 1])     # p[0] is the origin
            if I >= N or J >= M or not wm[I, J]:
                continue
            r = p[1:]
            mid = r[(r[:, 0] != 0) | (r[:, 1] != 0)].astype(int)
            c = cost + sum(w * lm[I - int(di), J - int(dj)] for di, dj, w in r)
            visit(I, J, c,
                  i1 + [I - d for d in mid[:, 0]] + [I],
                  i2 + [J - d for d in mid[:, 1]] + [J],
                  i1s + [I], i2s + [J], st + [k])

    visit(0, 0, lm[0, 0], [0], [0], [0], [0], [])
    return out


def key(p):
    g = (lambda f: p[f]) if isinstance(p, dict) else (lambda f: getattr(p, f))
    return tuple(tuple(int(x) for x in g(f)) for f in ["index1", "index2", "stepsTaken"])


def distance(p):
    return p["distance"] if isinstance(p, dict) else p.distance


class TestNearOptimalPaths(unittest.TestCase):

    def assertSamePaths(self, got, want):
        self.assertEqual(sorted(map(key, got)), sorted(map(key, want)))
        dg = [distance(p) for p in sorted(got, key=key)]
        dw = [distance(p) for p in sorted(want, key=key)]
        np.testing.assert_allclose(dg, dw)

    def check(self, a, threshold):
        want = [p for p in allPaths(a) if p["distance"] <= threshold + 1e-9]
        got = nearOptimalPaths(a, threshold)
        self.assertSamePaths(got, want)
        d = [p.distance for p in got]
        self.assertEqual(d, sorted(d))
        if len(got) > 0 and threshold >= a.distance:
            for f in FIELDS:
                assert_array_equal(getattr(got[0], f), getattr(a, f))
            self.assertEqual(got[0].distance, a.distance)
            assert_array_equal(got[0].normalizedDistance, a.normalizedDistance)
        return got

    def setUp(self):
        self.ds = dtw(np.arange(1, 8) + 2, np.arange(1, 9),
                      keep_internals=True, step_pattern=asymmetric)

    # Example from the documentation: all 126 paths, best first
    def test_documentation_example(self):
        k = nearOptimalPaths(self.ds, np.inf)
        self.assertEqual(len(k), countPaths(self.ds))
        self.assertEqual(len(k), 126)
        for f in FIELDS:
            assert_array_equal(getattr(k[0], f), getattr(self.ds, f))
        counts = np.unique([p.distance for p in k], return_counts=True)[1]
        assert_array_equal(counts, [1, 6, 10, 10, 11, 12, 13, 13, 12, 11, 9, 7, 5, 3, 2, 1])

    # Compare with the reference on small problems
    def test_against_enumeration(self):
        lm = np.random.default_rng(1).integers(0, 4, size=(5, 6)).astype(float)
        for sp in [symmetric1, symmetric2, asymmetric, asymmetricP05, typeIIIc, mori2006]:
            for win in ["none", "sakoechiba"]:
                with self.subTest(sp=sp, win=win):
                    a = dtw(lm, step_pattern=sp, keep_internals=True,
                            window_type=win,
                            window_args={} if win == "none" else {"window_size": 2})
                    d = sorted(p["distance"] for p in allPaths(a))
                    for threshold in [a.distance, d[len(d) // 3], np.inf]:
                        self.check(a, threshold)

    # Open end, also with a window: paths must not end outside it
    def test_open_end(self):
        lm = np.random.default_rng(1).integers(0, 4, size=(5, 6)).astype(float)
        for sp in [asymmetric, asymmetricP05]:
            for win in ["none", "sakoechiba"]:
                with self.subTest(sp=sp, win=win):
                    a = dtw(lm, step_pattern=sp, keep_internals=True, open_end=True,
                            window_type=win,
                            window_args={} if win == "none" else {"window_size": 1})
                    self.check(a, np.inf)
                    k = self.check(a, a.distance + 2)
                    for p in k:
                        self.assertAlmostEqual(p.normalizedDistance, p.distance / 5)
                        self.assertEqual(p.jmin, p.index2[-1])

    # Normalizations are those of dtw()
    def test_normalized_distance(self):
        q, r = dtw_test_data.sin_cos()
        for sp in [symmetric2, asymmetric, symmetric1]:
            a = dtw(q[:20], r[:25], step_pattern=sp, keep_internals=True)
            p = nearOptimalPaths(a)[0]
            if np.isnan(a.normalizedDistance):
                self.assertTrue(np.isnan(p.normalizedDistance))
            else:
                self.assertEqual(p.normalizedDistance, a.normalizedDistance)

    # Multi-step patterns list the intermediate cells, like dtw()
    def test_multistep(self):
        a = dtw([1, 2, 3], [1, 2, 3, 3], step_pattern=asymmetricP05, keep_internals=True)
        k = nearOptimalPaths(a)
        self.assertEqual(len(k), 1)
        assert_array_equal(k[0].index2, [0, 1, 2, 3])

    # The default threshold returns the optimum despite rounding errors
    def test_rounding(self):
        rng = np.random.default_rng(2)
        for i in range(20):
            a = dtw(rng.random(30), rng.random(25), step_pattern=asymmetricP05,
                    keep_internals=True)
            k = nearOptimalPaths(a)
            self.assertGreaterEqual(len(k), 1)
            for f in FIELDS:
                assert_array_equal(getattr(k[0], f), getattr(a, f))
            self.assertEqual(k[0].distance, a.distance)

    # Ties: on a flat cost matrix, all paths are optimal
    def test_ties(self):
        a = dtw(np.zeros((3, 3)), step_pattern=symmetric1, keep_internals=True)
        self.assertEqual(len(nearOptimalPaths(a)), countPaths(a))

    # Thresholds below the optimum give no paths
    def test_below_optimum(self):
        self.assertEqual(nearOptimalPaths(self.ds, self.ds.distance - 1), [])

    # The returned objects work with the plotting and warping functions
    def test_paths_are_alignments(self):
        k = nearOptimalPaths(self.ds, self.ds.distance + 1)
        for p in k:
            self.assertIsInstance(p, DTW)
            self.assertEqual((p.N, p.M), (7, 8))
            self.assertEqual(len(warp(p)), 8)

    def test_errors(self):
        with self.assertRaisesRegex(ValueError, "keep_internals"):
            nearOptimalPaths(dtw(np.arange(5), np.arange(6)))
        with self.assertRaisesRegex(ValueError, "max_paths"):
            nearOptimalPaths(self.ds, np.inf, max_paths=100)
        with self.assertRaisesRegex(ValueError, "Open-begin"):
            nearOptimalPaths(dtw(np.arange(3), np.arange(6), step_pattern=asymmetric,
                                 keep_internals=True, open_begin=True, open_end=True))
        with self.assertRaisesRegex(ValueError, "N-normalizable"):
            nearOptimalPaths(dtw(np.arange(3), np.arange(6), step_pattern=symmetricP2,
                                 keep_internals=True, open_end=True))
        with self.assertRaises(TypeError):
            nearOptimalPaths("not an alignment")
        for bad in [np.nan, "1", [1, 2], True]:
            with self.assertRaisesRegex(ValueError, "threshold"):
                nearOptimalPaths(self.ds, bad)
        for bad in [0, -1, np.nan, "10"]:
            with self.assertRaisesRegex(ValueError, "max_paths"):
                nearOptimalPaths(self.ds, max_paths=bad)

    # Patterns that computeCM() would misread are rejected
    def test_invalid_patterns(self):
        a = dtw(np.arange(4), np.arange(5), keep_internals=True)
        a.stepPattern = StepPattern(np.array([[1, 1, 1, 1], [1, 0, 0, -1]]))
        with self.assertRaisesRegex(ValueError, "origin"):
            nearOptimalPaths(a)
        a.stepPattern = StepPattern(np.array([[1, 1, 1, -1], [1, 0, 0, 1], [1, 1, 0, -1]]))
        with self.assertRaisesRegex(ValueError, "more than one origin"):
            nearOptimalPaths(a)


if __name__ == '__main__':
    unittest.main()
