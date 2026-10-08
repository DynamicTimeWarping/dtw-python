import sys
import sysconfig
import unittest
from concurrent.futures import ThreadPoolExecutor

import numpy as np
from numpy.testing import assert_array_equal
from dtw import *


FREETHREADED = bool(sysconfig.get_config_var("Py_GIL_DISABLED"))


def _align(job):
    x, y, sp = job
    a = dtw(x, y, step_pattern=sp, keep_internals=True)
    return a.distance, a.index1, a.index2, a.costMatrix


class TestThreads(unittest.TestCase):
    @unittest.skipUnless(FREETHREADED, "not a free-threaded build")
    def test_import_keeps_gil_disabled(self):
        # dtw is imported above; an extension not declared free-threading
        # compatible would have re-enabled the GIL
        self.assertFalse(sys._is_gil_enabled())

    def test_parallel_matches_serial(self):
        rng = np.random.default_rng(0)
        patterns = [symmetric2, asymmetric, rabinerJuangStepPattern(4, "c")]
        jobs = [(rng.random(400), rng.random(300), patterns[i % 3])
                for i in range(24)]
        serial = [_align(j) for j in jobs]
        with ThreadPoolExecutor(8) as ex:
            parallel = list(ex.map(_align, jobs))
        for s, p in zip(serial, parallel):
            self.assertEqual(s[0], p[0])
            for a, b in zip(s[1:], p[1:]):
                assert_array_equal(a, b)


if __name__ == '__main__':
    unittest.main()
