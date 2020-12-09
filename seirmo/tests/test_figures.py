#
# This file is part of seirmo (https://github.com/SABS-R3-Epidemiology/seirmo/)
# which is released under the BSD 3-clause license. See accompanying LICENSE.md
# for copyright notice and full license details.
#

import unittest
from unittest.mock import patch

import numpy as np
import pandas as pd

import seirmo as se


class TestIncidenceNumberPlot(unittest.TestCase):
    """
    Test the 'IncidenceNumberPlot' class.
    """
    def test__init__(self):
        se.IncidenceNumberPlot()

    def test_add_data(self):
        data = pd.DataFrame({
            'Time': [0, 1, 2, 3, 4, 5, 6],
            'Incidence Number': [1, 2, 3, 4, 5, 6, 7]}) # noqa
        time_key = 'Time'
        inc_key = 'Incidence Number'
        test_plot = se.IncidenceNumberPlot()
        test_plot.add_data(
            data, time_key=time_key, inc_key=inc_key)

        # Test the times in the figure is the same as what we give
        np.testing.assert_array_equal(
            test_plot._fig['data'][0]['x'],
            np.array([0, 1, 2, 3, 4, 5, 6]))

        # Test the incidences in the figure is the same as what we give
        np.testing.assert_array_equal(
            test_plot._fig['data'][0]['y'],
            np.array([1, 2, 3, 4, 5, 6, 7]))

        # Test that warning will be raised when x axis labels not match
        data2 = pd.DataFrame({
            'times': [0, 1, 2, 3, 4, 5, 6],
            'Incidence Number': [1, 2, 3, 4, 5, 6, 7]})
        time_key = 'times'
        inc_key = 'Incidence Number'

        with self.assertWarns(UserWarning):
            test_plot.add_simulation(
                data2, time_key=time_key, inc_key=inc_key)

        # Test that warning will be raised when y axis labels not match
        data3 = pd.DataFrame({
            'times': [0, 1, 2, 3, 4, 5, 6],
            'incidences': [1, 2, 3, 4, 5, 6, 7]})
        time_key = 'times'
        inc_key = 'incidences'

        with self.assertWarns(UserWarning):
            test_plot.add_simulation(
                data3, time_key=time_key, inc_key=inc_key)

    def test_add_simulation(self):
        data = pd.DataFrame({
            'Time': [0, 1, 2, 3, 4, 5, 6],
            'Incidence Number': [1, 2, 3, 4, 5, 6, 7]})
        time_key = 'Time'
        inc_key = 'Incidence Number'
        test_plot = se.IncidenceNumberPlot()
        test_plot.add_simulation(
            data, time_key=time_key, inc_key=inc_key)

        # Test the times in the figure is the same as what we give
        np.testing.assert_array_equal(
            test_plot._fig['data'][0]['x'],
            np.array([0, 1, 2, 3, 4, 5, 6]))

        # Test the incidences in the figure is the same as what we give
        np.testing.assert_array_equal(
            test_plot._fig['data'][0]['y'],
            np.array([1, 2, 3, 4, 5, 6, 7]))

        # Test that warning will be raised when x axis labels not match
        data2 = pd.DataFrame({
            'times': [0, 1, 2, 3, 4, 5, 6],
            'Incidence Number': [1, 2, 3, 4, 5, 6, 7]})
        time_key = 'times'
        inc_key = 'Incidence Number'

        with self.assertWarns(UserWarning):
            test_plot.add_simulation(
                data2, time_key=time_key, inc_key=inc_key)

        # Test that warning will be raised when y axis labels not match
        data3 = pd.DataFrame({
            'times': [0, 1, 2, 3, 4, 5, 6],
            'incidences': [1, 2, 3, 4, 5, 6, 7]})
        time_key = 'times'
        inc_key = 'incidences'

        with self.assertWarns(UserWarning):
            test_plot.add_simulation(
                data3, time_key=time_key, inc_key=inc_key)

    def test_show(self):
        test_plot = se.IncidenceNumberPlot()
        with patch('plotly.graph_objects.Figure.show') as show_patch:
            test_plot.show()
            assert show_patch.called


if __name__ == '__main__':
    unittest.main()
