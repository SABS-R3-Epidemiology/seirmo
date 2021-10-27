import unittest
import numpy as np
import numpy.testing as npt

import seirmo as se


class TestStochasticOutputCollector(unittest.TestCase):
    """
    Test the Output Collector for the Stochastic SEIR model
    """
    def test__init__(self):
        output = se.StochasticOutputCollector(['S', 'I', 'R'])
        self.assertEqual(output._output_names, ['S', 'I', 'R'])
        self.assertEqual(output._n_outputs, 3)
        npt.assert_array_equal(output._output_indices, np.arange(3))

    def test_begin(self):
        output = se.StochasticOutputCollector(['S', 'I', 'R'])
        output.begin(np.array([0]))
        npt.assert_array_equal(output._data, np.zeros((1,4)))
        self.assertEqual(output._data[:, 0], [0])
        self.assertEqual(output._index, 0)

    def test_report_and_retrieve_time(self):
        output = se.StochasticOutputCollector(['S', 'E', 'I', 'R'])
        output.begin(np.array([1, 2, 3]))

        #Checks that the input data is the right shape
        self.assertRaises(AssertionError, output.report, np.array([1, 2]))

        #Checks that report is storing the solution correctly 
        #and that retrieve is returning the correct part of the solution
        output.report(np.array([1, 2, 3, 4, 5]))
        output.report(np.array([2, 2, 3, 4, 5]))
        output.report(np.array([3, 2, 3, 4, 5]))
        output.report(np.array([4, 2, 3, 4, 5]))
        self.assertRaises(AssertionError, output.retrieve_time, 6)
        npt.assert_array_equal(output.retrieve_time(1), np.transpose([2, 2, 3, 4, 5]))

if __name__ == '__main__':
    unittest.main()
