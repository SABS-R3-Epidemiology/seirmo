#
# This file is part of seirmo (https://github.com/SABS-R3-Epidemiology/seirmo/)
# which is released under the BSD 3-clause license. See accompanying LICENSE.md
# for copyright notice and full license details.
#

import unittest

import seirmo as se


class TestSEIRForwardModel(unittest.TestCase):
    """
    Test the 'ForwardModel' class.
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


if __name__ == '__main__':
    unittest.main()
