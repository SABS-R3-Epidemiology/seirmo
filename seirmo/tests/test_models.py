#
# This file is part of seirmo (https://github.com/SABS-R3-Epidemiology/seirmo/)
# which is released under the BSD 3-clause license. See accompanying LICENSE.md
# for copyright notice and full license details.
#

import unittest
import seirmo as se


class TestForwardModelClass(unittest.TestCase):
    """
    Test the 'ForwardModel' class.
    """
    def test__init__(self):
        se.ForwardModel()

    def test_simulate(self):
        forward_model = se.ForwardModel()
        with self.assertRaises(NotImplementedError):
            forward_model.simulate(0, 1)

