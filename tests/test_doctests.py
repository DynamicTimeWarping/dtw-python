
import unittest
import doctest
import glob

def load_tests(loader, tests, ignore):
    fl=glob.glob("dtwr/*.py")
    tests.addTests(doctest.DocFileSuite(*fl,module_relative=False))
    return tests

