#
# This file is part of seirmo (https://github.com/SABS-R3-Epidemiology/seirmo.git) which is
# released under the BSD 3-clause license. See accompanying LICENSE.md for
# copyright notice and full license details.
#
#
import unittest

from seirmo.dummy import dummy_function


class TestDummyFunction(unittest.TestCase):
    '''
    Test Dummy function
    '''
    def test_output(self):
        self.assertEqual(dummy_function(), 42)
