#
# This file is part of seirmo (https://github.com/SABS-R3-Epidemiology/seirmo/)
# which is released under the BSD 3-clause license. See accompanying LICENSE.md
# for copyright notice and full license details.
#

import unittest
from unittest.mock import patch
import numpy as np
import numpy.testing as nptest
import seirmo as se


class TestStochModel(unittest.TestCase):
    """
    Test the 'StochasticSEIRModel' subclass.
    """
    def test__init__(self):
        model = se.StochasticSEIRModel([
            'S0', 'E0', 'I0', 'R0', 'beta', 'kappa', 'gamma'
        ])
        self.assertEqual(model.output_names(), [
            'S', 'E', 'I', 'R'
        ])
        self.assertEqual(model.parameter_names(), [
            'S0', 'E0', 'I0', 'R0', 'beta', 'kappa', 'gamma'
        ])
        self.assertEqual(model.n_outputs(), 4)
        self.assertEqual(model.n_parameters(), 7)
        np.testing.assert_array_equal(
            model._output_collector._output_indices, np.arange(4))

    def test_n_outputs(self):
        model = se.StochasticSEIRModel(np.zeros((4, 4)))
        self.assertEqual(model.n_outputs(), 4)

    def test_n_parameters(self):
        model = se.StochasticSEIRModel([
            'S0', 'E0', 'I0', 'R0', 'beta', 'kappa', 'gamma'
        ])
        self.assertEqual(model.n_parameters(), 7)

    def test_output_names(self):
        model = se.StochasticSEIRModel([
            'S0', 'E0', 'I0', 'R0', 'beta', 'kappa', 'gamma'
        ])
        self.assertEqual(model.output_names(), [
            'S', 'E', 'I', 'R'])

        model.set_outputs(['I'])
        self.assertEqual(model.output_names(), ['I'])

    def test_parameter_names(self):
        model = se.StochasticSEIRModel([
            'S0', 'E0', 'I0', 'R0', 'beta', 'kappa', 'gamma'
        ])
        self.assertEqual(model.parameter_names(), [
            'S0', 'E0', 'I0', 'R0', 'beta', 'kappa', 'gamma'
        ])

    def test_set_outputs(self):
        model = se.StochasticSEIRModel([
            'S0', 'E0', 'I0', 'R0', 'beta', 'kappa', 'gamma'
        ])

        # Check ValueError will be raised when some output names
        # are not as required
        with self.assertRaises(ValueError):
            model.set_outputs(['incidence number'])

        model.set_outputs(['I', 'R'])
        # Check the outputs names and number are as expected
        self.assertEqual(model._output_collector._output_indices, [2, 3])
        self.assertEqual(model.n_outputs(), 2)

    def test_propens_func(self):
        model = se.StochasticSEIRModel([
            'S0', 'E0', 'I0', 'R0', 'beta', 'kappa', 'gamma'
        ])
        #check it works
        initial_values = [0.9, 0, 0.1, 0]
        constants = [1, 1, 1]
        test_parameters = initial_values + constants
        model._parameters.configure_parameters(np.array(test_parameters))

        current_state = np.ones(5)
        model_prop = model.update_propensity(current_state)
        expected_propensity = np.array([[0, 1, 0, 0], [0, 0, 1, 0],
                                       [0, 0, 0, 1], [0, 0, 0, 0]])
        nptest.assert_array_equal(model_prop, expected_propensity)
        self.assertEqual(model_prop.shape, (4, 4))

        #check zeros

        current_state = np.zeros(5)
        model_prop = model.update_propensity(current_state)
        expected_propensity = np.zeros((4, 4))
        nptest.assert_array_equal(model_prop, expected_propensity)

    def test_simulate(self):
        model = se.StochasticSEIRModel([
            'S0', 'E0', 'I0', 'R0', 'beta', 'kappa', 'gamma'
        ])

        initial_values = [0.9, 0, 0.1, 0]
        constants = [1, 1, 1]
        test_parameters = initial_values + constants

        n_times = 10
        test_times = np.linspace(0, 10, num=n_times)
        model._parameters.configure_parameters(
            np.array(test_parameters))

        model.set_outputs(['S', 'I'])

        def inner(*args, **kwargs):
            for i in range(n_times):
                yield np.zeros((5,))
        with patch('seirmo._stoch_model.solve_gillespie',
                   side_effect=inner):
            output = model.simulate(np.array(test_parameters), test_times)

        # Check output shape
        self.assertEqual(output.shape, (n_times, 2))

        # Check positivity
        pos_matrix = (output >= 0)
        assert np.all(pos_matrix)


if __name__ == '__main__':
    unittest.main()
