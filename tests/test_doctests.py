
import unittest
import doctest
import glob
import os.path

import dtw


def run_suite():
    md = dtw.__path__[0]
    fl = glob.glob(os.path.join(md, "*.py"))
    suite = doctest.DocFileSuite(*fl, module_relative=False)
    return unittest.TextTestRunner(verbosity=2).run(suite)


class TestDoctests(unittest.TestCase):
    def test_doctests(self):
        r = run_suite()
        assert len(r.failures)==0


if __name__ == "__main__":
    run_suite()
