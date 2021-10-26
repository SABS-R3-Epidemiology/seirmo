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

numReps = 100


class TestGillespieFunc(unittest.TestCase):
    """Test the gillespie solve_gillespie function"""
    @classmethod
    def setUpClass(cls) -> None:
        cls.initial = np.array([10, 0])
        cls.t_span = [0, 10]
        cls.m = MagicMock()
        cls.m.return_value = np.array([[0, 1], [0, 0]])

    def test_t_span_input(self):
        with self.assertRaises(ValueError):  # t_span is 2D
            list(se.solve_gillespie(self.m, self.initial, t_span=[0]))
            # convert generator to list to force function to be evaluated#

        with self.assertRaises(ValueError):  # t_span must have range
            list(se.solve_gillespie(self.m, self.initial, t_span=[0, 0]))
        with self.assertRaises(ValueError):  # t_stop > t_start
            list(se.solve_gillespie(self.m, self.initial, t_span=[-2, 0]))
        with self.assertRaises(TypeError):  # time values must be floats
            list(se.solve_gillespie(self.m, self.initial, t_span=[0, 'ten']))

    @parameterized.expand([(random.random() * 100, random.random() * 100)
                           for _ in range(numReps)])
    def test_tspan_ordering(self, start, stop):
        test_span = [start, stop]
        if stop <= start:
            with self.assertRaises(ValueError):
                list(se.solve_gillespie(self.m, self.initial, test_span))

    def test_intial_input(self):
        with self.assertRaises(ValueError):  # initial conditions must be +ve
            list(se.solve_gillespie(self.m, np.array([-10, 0]), self.t_span))

    def test_propensity_call(self):
        m_count = MagicMock()
        m_count.return_value = np.array([[0, 1], [0, 0]])
        solve = se.solve_gillespie(m_count, self.initial, self.t_span)
        next(solve)  # return a yield
        self.assertEqual(m_count.call_count, 1,
                         'Propensity Func called unexpected number of times')
        next(solve)  # return a yield
        self.assertEqual(m_count.call_count, 2,
                         'Propensity Func called unexpected number of times')

    def test_gillespie_output(self):
        solution = list(se.solve_gillespie(self.m, self.initial, [0, 100]))
        self.assertTrue(np.all(np.array(solution) >= 0),
                        'Returned negative values in solution array')
        final_sol = solution[-1][1:]  # take only compartment nums at end
        self.assertEqual(final_sol.tolist(), [0, 10],
                         'Unexpected output - incomplete infection')

    @parameterized.expand([(np.random.randint(0, 100, (3,)),
                            np.random.rand(3, 3) * 100)
                           for _ in range(numReps)])
    def test_population_conservation(self, initial, propensity_mat):
        m_4dim = MagicMock()
        m_4dim.return_value = propensity_mat
        initial_pop = np.sum(initial)

        solve = se.solve_gillespie(m_4dim, initial, [0, 1])
        while True:
            try:
                output = next(solve)
            except StopIteration:
                break
            self.assertEqual(output.shape, (len(initial) + 1,),
                             'Unexpected number of output compartments')
            self.assertAlmostEqual(np.sum(output[1:]), initial_pop,
                                   'Unexpected output - pop. not conserved')


if __name__ == '__main__':
    unittest.main()
