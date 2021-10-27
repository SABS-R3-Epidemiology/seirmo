#
# This file is part of seirmo (https://github.com/SABS-R3-Epidemiology/seirmo/)
# which is released under the BSD 3-clause license. See accompanying LICENSE.md
# for copyright notice and full license details.
#

import unittest
import numpy as np
import seirmo as se


class TestSEIRForwardModel(unittest.TestCase):
    """
    Test the 'SEIRForwardModel' class.
    """
    def test__init__(self):
        se.SEIRForwardModel()

    def test_n_outputs(self):
        forward_model = se.SEIRForwardModel()
        with self.assertRaises(NotImplementedError):
            forward_model.n_outputs()

    def test_n_parameters(self):
        forward_model = se.SEIRForwardModel()
        with self.assertRaises(NotImplementedError):
            forward_model.n_parameters()

    def test_output_names(self):
        forward_model = se.SEIRForwardModel()
        with self.assertRaises(NotImplementedError):
            forward_model.output_names()

    def test_parameter_names(self):
        forward_model = se.SEIRForwardModel()
        with self.assertRaises(NotImplementedError):
            forward_model.parameter_names()

    def test_set_outputs(self):
        forward_model = se.SEIRForwardModel()
        with self.assertRaises(NotImplementedError):
            forward_model.set_outputs('S')

    def test_simulate(self):
        forward_model = se.SEIRForwardModel()
        with self.assertRaises(NotImplementedError):
            forward_model.simulate(0, 1)


class TestSEIRParameters(unittest.TestCase):
    """Tests the SEIRParameters Class"""
    def test__init__(self):
        se.SEIRParameters([])

    def test_configureParameters(self):
        testSubject = se.SEIRParameters(['a', 'b'])
        testSubject.configureParameters(np.zeros((2,)))

    def test_configureParametersError(self):
        testSubject = se.SEIRParameters(['a', 'b'])
        with self.assertRaises(AssertionError):
            testSubject.configureParameters(np.array([1, 2, 3]))

    def test__getitem__(self):
        testSubject = se.SEIRParameters(['a', 'b'])
        params = np.array([1, 2])
        testSubject.configureParameters(params)
        for i in range(params.shape[0]):
            self.assertEqual(params[i], testSubject[i])

    def test_n_parameters(self):
        testSubject = se.SEIRParameters(['a', 'b'])
        self.assertEqual(2, testSubject.n_parameters())

    def test_parameter_names(self):
        testSubject = se.SEIRParameters(['a', 'b'])
        self.assertEqual(['a', 'b'], testSubject.parameter_names())


class TestSEIROutputCollector(unittest.TestCase):
    """Tests the SEIROutputCollector Class"""
    def test__init__(self):
        se.SEIROutputCollector([])

    def test_n_outputs(self):
        testSubject = se.SEIROutputCollector(['a', 'b'])
        self.assertEqual(2, testSubject.n_outputs())

    def test_output_names(self):
        testSubject = se.SEIROutputCollector(['a', 'b'])
        self.assertEqual(['a', 'b'], testSubject.output_names())

    def test_set_outputs(self):
        testSubject = se.SEIROutputCollector(['a', 'b'])
        testSubject.set_outputs(['a'])

    def test_set_outputsFail(self):
        testSubject = se.SEIROutputCollector(['a', 'b'])
        self.assertRaises(ValueError, testSubject.set_outputs, ['c'])

    def test_report(self):
        testSubject = se.SEIROutputCollector(['a', 'b'])
        self.assertRaises(
            NotImplementedError,
            testSubject.report, np.zeros((2, 1)))


if __name__ == '__main__':
    unittest.main()
