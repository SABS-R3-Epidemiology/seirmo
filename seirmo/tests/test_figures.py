#
# This file is part of seirmo (https://github.com/SABS-R3-Epidemiology/seirmo/)
# which is released under the BSD 3-clause license. See accompanying LICENSE.md
# for copyright notice and full license details.
#

import unittest

import numpy as np
import pandas as pd

import seirmo as se


class IncidenceNumberPlot(unittest.TestCase):
    """
    Test the 'IncidenceNumberPlot' class.
    """
    def test__init__(self):
        se.IncidenceNumberPlot()

    def test_add_data(self):
        pandas_DataFrame = pd.DataFrame({'Time': [0, 1, 2, 3, 4, 5, 6],
                                         'Incidence Number': [1, 2, 3, 4, 5, 6, 7]}) # noqa
        time_key = 'Time'
        inc_key = 'Incidence Number'
        test_plot = se.IncidenceNumberPlot()
        test_plot.add_data(pandas_DataFrame, time_key=time_key,
                           inc_key=inc_key)

        # Test the data in the figure is the same as what we give
        np.testing.assert_array_equal(
            np.array(
                [test_plot._fig['data'][0]['x'],
                 test_plot._fig['data'][0]['y']]),
            np.array(
                [np.array([0, 1, 2, 3, 4, 5, 6]),
                 np.array([1, 2, 3, 4, 5, 6, 7])])
        )

    def test_add_simulation(self):
        pandas_DataFrame = pd.DataFrame({'Time': [0, 1, 2, 3, 4, 5, 6],
                                         'Incidence Number': [1, 2, 3, 4, 5, 6, 7]}) # noqa
        time_key = 'Time'
        inc_key = 'Incidence Number'
        test_plot = se.IncidenceNumberPlot()
        test_plot.add_simulation(pandas_DataFrame, time_key=time_key,
                                 inc_key=inc_key)

        # Test the data in the figure is the same as what we give
        np.testing.assert_array_equal(
            np.array(
                [test_plot._fig['data'][0]['x'],
                 test_plot._fig['data'][0]['y']]),
            np.array(
                [np.array([0, 1, 2, 3, 4, 5, 6]),
                 np.array([1, 2, 3, 4, 5, 6, 7])])
        )
