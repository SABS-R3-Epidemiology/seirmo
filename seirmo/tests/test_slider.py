#
# This file is part of seirmo (https://github.com/SABS-R3-Epidemiology/seirmo/)
# which is released under the BSD 3-clause license. See accompanying LICENSE.md
# for copyright notice and full license details.
#

import numpy as np

import unittest
import seirmo as se


class TestSliderComponent(unittest.TestCase):
    """
    Test the '_SliderComponent' class.
    """
    def test__init__(self):


    def test_add_slider(self):

        model = se.SEIRModel
        simulation = se.SimulationController(model, start, end)

        output = simulation.run(test_parameters, return_incidence=True)

        # Check output shape
        self.assertEqual(output.shape, (50, n_outputs + 1))

        # Check that sum of states is one at all times
        output = simulation.run(test_parameters)
        total = np.sum(output, axis=1)
        expected = np.ones(shape=50)
        np.testing.assert_almost_equal(total, expected)

    def test_group_sliders(self):


    def test_slider_ids(self):
        


if __name__ == '__main__':
    unittest.main()
