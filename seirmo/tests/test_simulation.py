#
# This file is part of seirmo (https://github.com/SABS-R3-Epidemiology/seirmo/)
# which is released under the BSD 3-clause license. See accompanying LICENSE.md
# for copyright notice and full license details.
#


import unittest
import seirmo as se


class TestSimulationController(unittest.TestCase):
    """
    Test the 'SimulationController' class.
    """
    def test__init__(self):
        start = 0
        end = 3
        with self.assertRaises(TypeError):
            se.SimulationController('ForwardModel', start, end)

    def test_simulate(self):

        start = 0
        end = 10
        simulation = se.SimulationController(se.ForwardModel, start, end)

        initial_values = [0.9, 0, 0.1, 0]
        constants = [1, 1, 1]
        test_parameters = initial_values + constants
        simulation.run(test_parameters)



if __name__ == '__main__':
    unittest.main()