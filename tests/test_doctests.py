
import unittest
import doctest
import glob
import os.path

import dtw
md = dtw.__path__[0]

def load_tests(loader, tests, ignore):
    fl=glob.glob(os.path.join(md,"*.py"))
    tests.addTests(doctest.DocFileSuite(*fl,module_relative=False))
    return tests

