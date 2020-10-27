import unittest

from seirmo.dummy import dummy_function

class TestDummyFunction(unittest.TestCase):
    '''
    Test Dummy function
    '''
    def test_output(self):
        self.assertEqual(dummy_function(),42)