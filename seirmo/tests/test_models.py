#
# This file is part of seirmo (https://github.com/SABS-R3-Epidemiology/seirmo/)
# which is released under the BSD 3-clause license. See accompanying LICENSE.md
# for copyright notice and full license details.
#

import unittest

import numpy as np

import seirmo as se


class TestForwardModel(unittest.TestCase):
    """
    Test the 'ForwardModel' class.
    """
    def test__init__(self):
        se.ForwardModel()

    def test_simulate(self):
        forward_model = se.ForwardModel()
        with self.assertRaises(NotImplementedError):
            forward_model.simulate(0, 1)


class TestSEIRModel(unittest.TestCase):
    """
    Test the 'ForwardModel' class.
    """
    def test__init__(self):
        se.SEIRModel()

    def test_simulate(self):
        model = se.SEIRModel()
        n_outputs = 4

        initial_values = [0.9, 0, 0.1, 0]
        constants = [1, 1, 1]
        test_parameters = initial_values + constants

        n_times = 10
        test_times = np.linspace(0, 10, num=n_times)

        # Test the case when return_incidence=False
        output = model.simulate(test_parameters, test_times)

        # Check output shape
        self.assertEqual(output.shape, (n_times, n_outputs))

        # Check that sum of states is one at all times
        total = np.sum(output, axis=1)
        expected = np.ones(shape=n_times)
        np.testing.assert_almost_equal(total, expected)

    def test_simulate_return_incidence_true(self):
        model = se.SEIRModel()

        initial_values = [0.9, 0, 0.1, 0]
        constants = [1, 1, 1]
        test_parameters = initial_values + constants

        n_times = 10
        test_times = np.linspace(0, 10, num=n_times)

        # Test the case when return_incidence=True
        output = model.simulate(
            test_parameters, test_times, return_incidence=True)

        # Check output shape
        n_outputs = 5
        self.assertEqual(output.shape, (n_times, n_outputs))

        # Check that sum of states is one at all times
        total = np.sum(output[:, :-1], axis=1)
        expected = np.ones(shape=n_times)
        np.testing.assert_almost_equal(total, expected)


if __name__ == '__main__':
    unittest.main()
