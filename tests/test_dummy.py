try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

import sys
import unittest

class TestDummy(unittest.TestCase):
    def setUp(self):
        self.held, sys.stdout = sys.stdout, StringIO()

    def test_dummy(self):
        self.assertTrue(True)
