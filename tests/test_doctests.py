
import unittest
import doctest
import glob
import os.path

import dtw


class TestDoctests(unittest.TestCase):
    def test_doctests(self):
        unittest.TextTestRunner(verbosity=2).run(suite()) 
        


def suite():
    md = dtw.__path__[0]
    fl=glob.glob(os.path.join(md,"*.py"))
    suite=doctest.DocFileSuite(*fl,module_relative=False)
    return suite

if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(suite()) 


