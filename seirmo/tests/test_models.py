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

        model.set_outputs(['I', 'Incidence'])
        self.assertEqual(model.output_names(), ['I', 'Incidence'])

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

    @classmethod
    def setUpClass(cls):
        cls.reduced_model = se.ReducedModel(se.SEIRModel())

    def test__init__(self):

        with self.assertRaises(TypeError):
            se.ReducedModel('1')

        # Test defaults
        self.assertEqual(self.reduced_model.n_parameters(), 7)
        self.assertEqual(
            self.reduced_model.parameter_names(),
            ['S0', 'E0', 'I0', 'R0', 'alpha', 'beta', 'gamma']
        )

    def test_fix_parameters(self):
        # Test error will be raised when the input is not a dictionary
        with self.assertRaises(ValueError):
            self.reduced_model.fix_parameters(name_value_dict=1)

    def test_n_fixed_parameters(self):
        # Test the number of fixed parameters is as expected
        # Test the case when self._fixed_params_mask is None:
        self.assertEqual(self.reduced_model.n_fixed_parameters(), 0)
        name_value_dict = {'S0': 0.5, 'alpha': 1}
        self.reduced_model.fix_parameters(name_value_dict)
        self.assertEqual(self.reduced_model.n_fixed_parameters(), 2)
        name_value_dict = {'E0': 0.5}
        self.reduced_model.fix_parameters(name_value_dict)
        self.assertEqual(self.reduced_model.n_fixed_parameters(), 3)

        # Unfix the parameters
        name_value_dict = {'S0': None, 'alpha': None, 'E0': None}
        self.reduced_model.fix_parameters(name_value_dict)

    def test_n_outputs(self):
        self.assertEqual(self.reduced_model.n_outputs(), 5)

    def test_n_parameters(self):
        # Test the number of (unfixed) parameters is as expected

        # The case when the mask is None
        self.assertEqual(self.reduced_model.n_parameters(), 7)

        name_value_dict = {'S0': 0.5, 'alpha': 1}
        self.reduced_model.fix_parameters(name_value_dict)
        self.assertEqual(self.reduced_model.n_parameters(), 5)
        name_value_dict = {'E0': 0.5}
        self.reduced_model.fix_parameters(name_value_dict)
        self.assertEqual(self.reduced_model.n_parameters(), 4)

        # Unfix the parameters
        name_value_dict = {'S0': None, 'E0': None, 'alpha': None}
        self.reduced_model.fix_parameters(name_value_dict)

    def test_output_names(self):
        # Test the output names are as expected
        self.assertEqual(self.reduced_model.output_names(), [
            'S', 'E', 'I', 'R', 'Incidence'
        ])

        self.reduced_model.set_outputs(['I', 'Incidence'])
        self.assertEqual(self.reduced_model.output_names(), ['I', 'Incidence'])

        # Set the outputs to the default
        self.reduced_model.set_outputs(
            ['S', 'E', 'I', 'R', 'Incidence'])

    def test_parameter_names(self):
        # Test the parameter names are as expected
        name_value_dict = {'S0': 0.5, 'alpha': 1}
        self.reduced_model.fix_parameters(name_value_dict)
        self.assertEqual(
            self.reduced_model.parameter_names(),
            ['E0', 'I0', 'R0', 'beta', 'gamma'])

        name_value_dict = {'E0': 0.5}
        self.reduced_model.fix_parameters(name_value_dict)
        self.assertEqual(
            self.reduced_model.parameter_names(),
            ['I0', 'R0', 'beta', 'gamma'])

        # Unfix the parameters
        name_value_dict = {'S0': None, 'E0': None, 'alpha': None}
        self.reduced_model.fix_parameters(name_value_dict)

    def test_set_outputs(self):

        # Check ValueError will be raised when some output names
        # are not as required
        with self.assertRaises(ValueError):
            self.reduced_model.set_outputs(['incidence number'])

        self.reduced_model.set_outputs(['I', 'Incidence'])
        # Check the outputs names and number are as expected
        self.assertEqual(self.reduced_model.output_names(), ['I', 'Incidence'])
        self.assertEqual(self.reduced_model.n_outputs(), 2)

        # Set the outputs to the default
        self.reduced_model.set_outputs(
            ['S', 'E', 'I', 'R', 'Incidence'])

    def test_simulate(self):
        initial_values = [0, 0.1, 0]
        constants = [1, 1]
        test_parameters = initial_values + constants

        n_times = 10
        test_times = np.linspace(0, 10, num=n_times)

        self.reduced_model.set_outputs(['S', 'I', 'Incidence'])
        self.reduced_model.fix_parameters({'S0': 0.9, 'alpha': 1})
        output = self.reduced_model.simulate(test_parameters, test_times)

        # Check output shape
        self.assertEqual(output.shape, (n_times, 3))

        # Check that sum of states is one at all times
        self.reduced_model.set_outputs(['S', 'E', 'I', 'R'])
        output = self.reduced_model.simulate(test_parameters, test_times)
        total = np.sum(output, axis=1)
        expected = np.ones(shape=n_times)
        np.testing.assert_almost_equal(total, expected)

        # Check output shape
        self.assertEqual(output.shape, (n_times, 4))

        # Check that the results are the same for the reduced model
        # and the normal model with the same parameters

        # Run the reduced model for all the outputs
        self.reduced_model.set_outputs(['S', 'E', 'I', 'R', 'Incidence'])
        output_reduced = self.reduced_model.simulate(
            test_parameters, test_times)

        # Run the normal model for all the outputs
        model = se.SEIRModel()

        initial_values = [0.9, 0, 0.1, 0]
        constants = [1, 1, 1]
        test_parameters = initial_values + constants

        np.testing.assert_almost_equal(total, expected)

        model.set_outputs(['S', 'E', 'I', 'R', 'Incidence'])
        output_normal = model.simulate(test_parameters, test_times)

        np.testing.assert_almost_equal(output_reduced, output_normal)

        # Set the outputs to the default
        self.reduced_model.set_outputs(
            ['S', 'E', 'I', 'R', 'Incidence'])

        # Unfix the parameters
        name_value_dict = {'S0': None, 'alpha': None}
        self.reduced_model.fix_parameters(name_value_dict)


if __name__ == '__main__':
    unittest.main()
