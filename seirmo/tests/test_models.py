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

    def test_n_outputs(self):
        forward_model = se.ForwardModel()
        with self.assertRaises(NotImplementedError):
            forward_model.n_outputs()

    def test_n_parameters(self):
        forward_model = se.ForwardModel()
        with self.assertRaises(NotImplementedError):
            forward_model.n_parameters()

    def test_output_names(self):
        forward_model = se.ForwardModel()
        with self.assertRaises(NotImplementedError):
            forward_model.output_names()

    def test_parameter_names(self):
        forward_model = se.ForwardModel()
        with self.assertRaises(NotImplementedError):
            forward_model.parameter_names()

    def test_set_outputs(self):
        forward_model = se.ForwardModel()
        with self.assertRaises(NotImplementedError):
            forward_model.set_outputs('S')

    def test_simulate(self):
        forward_model = se.ForwardModel()
        with self.assertRaises(NotImplementedError):
            forward_model.simulate(0, 1)


class TestSEIRModel(unittest.TestCase):
    """
    Test the 'ForwardModel' class.
    """
    def test__init__(self):
        model = se.SEIRModel()
        self.assertEqual(model._output_names, [
            'S', 'E', 'I', 'R', 'Incidence'
        ])
        self.assertEqual(model._parameter_names, [
            'S0', 'E0', 'I0', 'R0', 'alpha', 'beta', 'gamma'
        ])
        self.assertEqual(model._n_outputs, 5)
        self.assertEqual(model._n_parameters, 7)
        np.testing.assert_array_equal(model._output_indices, np.arange(5))

    def test_n_outputs(self):
        model = se.SEIRModel()
        self.assertEqual(model.n_outputs(), 5)

    def test_n_parameters(self):
        model = se.SEIRModel()
        self.assertEqual(model.n_parameters(), 7)

    def test_output_names(self):
        model = se.SEIRModel()
        self.assertEqual(model.output_names(), [
            'S', 'E', 'I', 'R', 'Incidence'
        ])

    def test_parameter_names(self):
        model = se.SEIRModel()
        self.assertEqual(model.parameter_names(), [
            'S0', 'E0', 'I0', 'R0', 'alpha', 'beta', 'gamma'
        ])

    def test_set_outputs(self):
        model = se.SEIRModel()

        # Check ValueError will be raised when some output names
        # are not as required
        with self.assertRaises(ValueError):
            model.set_outputs(['incidence number'])

        model.set_outputs(['I', 'Incidence'])
        # Check the outputs names and number are as expected
        self.assertEqual(model._output_indices, [2, 4])
        self.assertEqual(model._n_outputs, 2)

    def test_simulate(self):
        model = se.SEIRModel()

        initial_values = [0.9, 0, 0.1, 0]
        constants = [1, 1, 1]
        test_parameters = initial_values + constants

        n_times = 10
        test_times = np.linspace(0, 10, num=n_times)

        model.set_outputs(['S', 'I', 'Incidence'])
        output = model.simulate(test_parameters, test_times)

        # Check output shape
        self.assertEqual(output.shape, (n_times, 3))

        # Check that sum of states is one at all times
        model.set_outputs(['S', 'E', 'I', 'R'])
        output = model.simulate(test_parameters, test_times)
        total = np.sum(output, axis=1)
        expected = np.ones(shape=n_times)
        np.testing.assert_almost_equal(total, expected)

        # Check output shape
        self.assertEqual(output.shape, (n_times, 4))


class TestReducedModel(unittest.TestCase):
    """
    Test the 'ReducedModel' class.
    """
    def test__init__(self):

        with self.assertRaises(TypeError):
            se.ReducedModel('1')

        # reduced_model = se.ReducedModel(se.ForwardModel())
        # self.assertEqual(reduced_model._model, se.ForwardModel())


if __name__ == '__main__':
    unittest.main()
