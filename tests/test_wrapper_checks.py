import unittest

import numpy as np
from dtw import *
from dtw._dtw_utils import _computeCM_wrapper


# symmetric1, as passed to the C core (column-major rows of the pattern)
SYM1 = np.array((1, 1, 2, 2, 3, 3, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, -1, 1, -1, 1, -1, 1),
                dtype=np.double)


def _call(wm_shape=(3, 3), lm_shape=(3, 3), cm_shape=(3, 3), dir=SYM1, nsteps=6):
    cm = np.full(cm_shape, np.nan)
    cm[0, 0] = 1
    return _computeCM_wrapper(np.ones(wm_shape, dtype=np.int32),
                              np.ones(lm_shape),
                              np.array([nsteps], dtype=np.int32),
                              np.asarray(dir, dtype=np.double),
                              cm)


class TestWrapperChecks(unittest.TestCase):
    def test_valid_call(self):
        out = _call()
        self.assertEqual(out['costMatrix'][2, 2], 3)

    def test_shape_mismatch_raises(self):
        with self.assertRaises(ValueError):
            _call(wm_shape=(3, 4))
        with self.assertRaises(ValueError):
            _call(cm_shape=(4, 3))

    def test_step_pattern_length_raises(self):
        with self.assertRaises(ValueError):
            _call(dir=SYM1[:-1], nsteps=6)

    def test_bad_pattern_numbers_raise(self):
        bad = SYM1.copy()
        bad[0] = 0          # pattern numbers start at 1
        with self.assertRaises(ValueError):
            _call(dir=bad)
        bad = SYM1.copy()
        bad[:6] = (2, 2, 1, 1, 3, 3)    # not ascending
        with self.assertRaises(ValueError):
            _call(dir=bad)

    def test_malformed_steppattern_raises_not_exits(self):
        sp = StepPattern(np.array([[0, 1, 1, -1], [0, 0, 0, 1]]), "NA")
        with self.assertRaises(ValueError):
            dtw(np.arange(5.), np.arange(5.), step_pattern=sp)


if __name__ == '__main__':
    unittest.main()
