#
# This file is part of seirmo (https://github.com/SABS-R3-Epidemiology/seirmo/)
# which is released under the BSD 3-clause license. See accompanying LICENSE.md
# for copyright notice and full license details.
#

import unittest
import numpy as np
from parameterized import parameterized
import random
from unittest.mock import MagicMock

import seirmo as se


class TestGillespieFunc(unittest.TestCase):
    """Test the gillespie solve_gillespie function"""
    @classmethod
    def setUpClass(cls) -> None:
        cls.initial = [10, 0]
        cls.t_span = [0, 1]
        cls.f = MagicMock()
        cls.f.return_value = np.array([[0, 1], [0, 0]])

    def test_t_span_input(self):
        se.solve_gillespie(self.f, self.initial, t_span=[-2, 0])
        with self.assertRaises(ValueError):
            se.solve_gillespie(self.f, self.initial, t_span=[-2, 0])


if __name__ == '__main__':
    unittest.main()
