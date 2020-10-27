import unittest

from seirmo.dummy import dummy_function

class TestDummyFunction(unittest.TestCase):
    def test_output(self):
        self.assertEqual(dummy_function(),42)