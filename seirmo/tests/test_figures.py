#
# This file is part of seirmo (https://github.com/SABS-R3-Epidemiology/seirmo/)
# which is released under the BSD 3-clause license. See accompanying LICENSE.md
# for copyright notice and full license details.
#

import unittest
from unittest.mock import patch

import numpy as np
import pandas as pd

from seirmo import plots


class TestIncidenceNumberPlot(unittest.TestCase):
    """
    Test the 'IncidenceNumberPlot' class.
    """
    def test__init__(self):
        plots.IncidenceNumberPlot()

    def test_add_data(self):
        data = pd.DataFrame({
            'Time': [0, 1, 2, 3, 4, 5, 6],
            'Incidence Number': [1, 2, 3, 4, 5, 6, 7]}) # noqa
        time_key = 'Time'
        inc_key = 'Incidence Number'
        test_plot = plots.IncidenceNumberPlot()
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
        test_plot = plots.IncidenceNumberPlot()
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


class TestCompartmentPlot(unittest.TestCase):
    """
    Test the 'CompartmentPlot' class.
    """
    def test__init__(self):
        plots.CompartmentPlot()

    def test_add_simulation(self):
        data = pd.DataFrame({
            'Time': [0, 1, 2, 3, 4, 5, 6],
            'Susceptible': [1, 2, 3, 4, 5, 6, 7],
            'Exposed': [2, 3, 4, 5, 6, 7, 8],
            'Infectious': [3, 4, 5, 6, 7, 8, 9],
            'Recovered': [4, 5, 6, 7, 8, 9, 10]})
        time_key = 'Time'
        compartment_keys = [
            'Susceptible', 'Exposed', 'Infectious', 'Recovered']
        test_plot = plots.CompartmentPlot()
        test_plot.add_simulation(
            data, time_key=time_key, compartment_keys=compartment_keys)

        # Test the times in the figure is the same as what we give
        np.testing.assert_array_equal(
            test_plot._fig['data'][0]['x'],
            np.array([0, 1, 2, 3, 4, 5, 6]))
        np.testing.assert_array_equal(
            test_plot._fig['data'][1]['x'],
            np.array([0, 1, 2, 3, 4, 5, 6]))
        np.testing.assert_array_equal(
            test_plot._fig['data'][2]['x'],
            np.array([0, 1, 2, 3, 4, 5, 6]))
        np.testing.assert_array_equal(
            test_plot._fig['data'][3]['x'],
            np.array([0, 1, 2, 3, 4, 5, 6]))

        # Test the S, E, I, R in the figure is the same as what we give
        np.testing.assert_array_equal(
            test_plot._fig['data'][0]['y'],
            np.array([1, 2, 3, 4, 5, 6, 7]))
        np.testing.assert_array_equal(
            test_plot._fig['data'][1]['y'],
            np.array([2, 3, 4, 5, 6, 7, 8]))
        np.testing.assert_array_equal(
            test_plot._fig['data'][2]['y'],
            np.array([3, 4, 5, 6, 7, 8, 9]))
        np.testing.assert_array_equal(
            test_plot._fig['data'][3]['y'],
            np.array([4, 5, 6, 7, 8, 9, 10]))

        # Test that warning will be raised when x axis labels not match
        data2 = pd.DataFrame({
            'times': [0, 1, 2, 3, 4, 5, 6],
            'Susceptible': [1, 2, 3, 4, 5, 6, 7],
            'Exposed': [2, 3, 4, 5, 6, 7, 8],
            'Infectious': [3, 4, 5, 6, 7, 8, 9],
            'Recovered': [4, 5, 6, 7, 8, 9, 10]})
        time_key = 'times'
        compartment_keys = [
            'Susceptible', 'Exposed', 'Infectious', 'Recovered']

        with self.assertWarns(UserWarning):
            test_plot.add_simulation(
                data2, time_key=time_key, compartment_keys=compartment_keys)

    def test_show(self):
        test_plot = se.CompartmentPlot()
        with patch('plotly.graph_objects.Figure.show') as show_patch:
            test_plot.show()
            assert show_patch.called

class TestSubplotFigure(unittest.TestCase):
    """
    Test the 'SubplotFigure' class.
    """
    def test__init__(self):
        plots.SubplotFigure()

    def test_get_layout(self):
        test_plot = plots.SubplotFigure()
        data = pd.DataFrame({
            'Time': [0, 1, 2, 3, 4, 5, 6],
            'Incidence Number': [1, 2, 3, 4, 5, 6, 7],
            'Susceptible': [1, 2, 3, 4, 5, 6, 7],
            'Exposed': [2, 3, 4, 5, 6, 7, 8],
            'Infectious': [3, 4, 5, 6, 7, 8, 9],
            'Recovered': [4, 5, 6, 7, 8, 9, 10]})
        test_plot._incidence_num_plot.add_simulation(data)
        test_plot._compartment_plot.add_simulation(data)
        test_plot._get_layout

        # Test the layouts of the subplots are as expected
        # Test the layout of the IncidenceNumberPlot is as expected
        np.testing.assertEqual(
            test_plot._fig[0]['layout']['xaxis']['title']['text'],
            'Time'
        )
        np.testing.assertEqual(
            test_plot._fig[0]['layout']['yaxis']['title']['text'],
            'Incidence Number'
        )

        # Test the layout of the CompartmentPlot is as expected
        np.testing.assertEqual(
            test_plot._fig[1]['layout']['xaxis']['title']['text'],
            'Time'
        )
        np.testing.assertEqual(
            test_plot._fig[1]['layout']['yaxis']['title']['text'],
            'Percentage in population'
        )

    def test_get_trace(self):

        test_plot = plots.SubplotFigure()
        data = pd.DataFrame({
            'Time': [0, 1, 2, 3, 4, 5, 6],
            'Incidence Number': [1, 2, 3, 4, 5, 6, 7],
            'Susceptible': [1, 2, 3, 4, 5, 6, 7],
            'Exposed': [2, 3, 4, 5, 6, 7, 8],
            'Infectious': [3, 4, 5, 6, 7, 8, 9],
            'Recovered': [4, 5, 6, 7, 8, 9, 10]})
        test_plot._incidence_num_plot.add_simulation(data)
        test_plot._compartment_plot.add_simulation(data)
        test_plot._get_trace

        # Test the data in the subplots are as expected
        # Test the data in the IncidenceNumberPlot is as expected
        # Test the times in the IncidenceNumberPlot is the same as what we give
        np.testing.assert_array_equal(
            test_plot._fig[0]['data'][0]['x'],
            np.array([0, 1, 2, 3, 4, 5, 6]))

        # Test the incidences in the IncidenceNumberPlot is the same as what we give
        np.testing.assert_array_equal(
            test_plot._fig[0]['data'][0]['y'],
            np.array([1, 2, 3, 4, 5, 6, 7]))
        
        # Test the times in the CompartmentPlot is the same as what we give
        np.testing.assert_array_equal(
            test_plot._fig[1]['data'][0]['x'],
            np.array([0, 1, 2, 3, 4, 5, 6]))
        np.testing.assert_array_equal(
            test_plot._fig[1]['data'][1]['x'],
            np.array([0, 1, 2, 3, 4, 5, 6]))
        np.testing.assert_array_equal(
            test_plot._fig[1]['data'][2]['x'],
            np.array([0, 1, 2, 3, 4, 5, 6]))
        np.testing.assert_array_equal(
            test_plot._fig[1]['data'][3]['x'],
            np.array([0, 1, 2, 3, 4, 5, 6]))

        # Test the S, E, I, R in the CompartmentPlot is the same as what we give
        np.testing.assert_array_equal(
            test_plot._fig[1]['data'][0]['y'],
            np.array([1, 2, 3, 4, 5, 6, 7]))
        np.testing.assert_array_equal(
            test_plot._fig[1]['data'][1]['y'],
            np.array([2, 3, 4, 5, 6, 7, 8]))
        np.testing.assert_array_equal(
            test_plot._fig[1]['data'][2]['y'],
            np.array([3, 4, 5, 6, 7, 8, 9]))
        np.testing.assert_array_equal(
            test_plot._fig[1]['data'][3]['y'],
            np.array([4, 5, 6, 7, 8, 9, 10]))

    def test_add_data(self):
        test_plot = plots.SubplotFigure()
        data = pd.DataFrame({
            'Time': [0, 1, 2, 3, 4, 5, 6],
            'Incidence Number': [1, 2, 3, 4, 5, 6, 7]})
        test_plot.add_data(data)

        # Test the layout of the subplot (IncidenceNumberPlot)
        # for the added data is as expected
        np.testing.assertEqual(
            test_plot._fig[0]['layout']['xaxis']['title']['text'],
            'Time'
        )
        np.testing.assertEqual(
            test_plot._fig[0]['layout']['yaxis']['title']['text'],
            'Incidence Number'
        )

        # Test the added data in the subplot (IncidenceNumberPlot)
        # is as expected
        # Test the times in the IncidenceNumberPlot is the same as what we give
        np.testing.assert_array_equal(
            test_plot._fig[0]['data'][0]['x'],
            np.array([0, 1, 2, 3, 4, 5, 6]))

        # Test the incidences in the IncidenceNumberPlot is the same as what we give
        np.testing.assert_array_equal(
            test_plot._fig[0]['data'][0]['y'],
            np.array([1, 2, 3, 4, 5, 6, 7]))
        
    def test_add_simulation(self):
        test_plot = plots.SubplotFigure()
        data = pd.DataFrame({
            'Time': [0, 1, 2, 3, 4, 5, 6],
            'Incidence Number': [1, 2, 3, 4, 5, 6, 7],
            'Susceptible': [1, 2, 3, 4, 5, 6, 7],
            'Exposed': [2, 3, 4, 5, 6, 7, 8],
            'Infectious': [3, 4, 5, 6, 7, 8, 9],
            'Recovered': [4, 5, 6, 7, 8, 9, 10]})
        test_plot.add_simulation(data)

        # Test the layout of the subplot (IncidenceNumberPlot)
        # for the added simulation data is as expected
        np.testing.assertEqual(
            test_plot._fig[0]['layout']['xaxis']['title']['text'],
            'Time'
        )
        np.testing.assertEqual(
            test_plot._fig[0]['layout']['yaxis']['title']['text'],
            'Incidence Number'
        )

        # Test the added simulation data in the subplot (IncidenceNumberPlot)
        # is as expected
        # Test the times in the IncidenceNumberPlot is the same as what we give
        np.testing.assert_array_equal(
            test_plot._fig[0]['data'][0]['x'],
            np.array([0, 1, 2, 3, 4, 5, 6]))

        # Test the incidences in the IncidenceNumberPlot is the same as what we give
        np.testing.assert_array_equal(
            test_plot._fig[0]['data'][0]['y'],
            np.array([1, 2, 3, 4, 5, 6, 7]))
        
        # Test the layout of the subplot (CompartmentPlot)
        # for the added simulation data is as expected
        np.testing.assertEqual(
            test_plot._fig[1]['layout']['xaxis']['title']['text'],
            'Time'
        )
        np.testing.assertEqual(
            test_plot._fig[1]['layout']['yaxis']['title']['text'],
            'Percentage in population'
        )

        # Test the added simulation data in the subplot (CompartmentPlot)
        # is as expected
        # Test the times in the CompartmentPlot is the same as what we give
        np.testing.assert_array_equal(
            test_plot._fig[1]['data'][0]['x'],
            np.array([0, 1, 2, 3, 4, 5, 6]))
        np.testing.assert_array_equal(
            test_plot._fig[1]['data'][1]['x'],
            np.array([0, 1, 2, 3, 4, 5, 6]))
        np.testing.assert_array_equal(
            test_plot._fig[1]['data'][2]['x'],
            np.array([0, 1, 2, 3, 4, 5, 6]))
        np.testing.assert_array_equal(
            test_plot._fig[1]['data'][3]['x'],
            np.array([0, 1, 2, 3, 4, 5, 6]))

        # Test the S, E, I, R in the CompartmentPlot is the same as what we give
        np.testing.assert_array_equal(
            test_plot._fig[1]['data'][0]['y'],
            np.array([1, 2, 3, 4, 5, 6, 7]))
        np.testing.assert_array_equal(
            test_plot._fig[1]['data'][1]['y'],
            np.array([2, 3, 4, 5, 6, 7, 8]))
        np.testing.assert_array_equal(
            test_plot._fig[1]['data'][2]['y'],
            np.array([3, 4, 5, 6, 7, 8, 9]))
        np.testing.assert_array_equal(
            test_plot._fig[1]['data'][3]['y'],
            np.array([4, 5, 6, 7, 8, 9, 10]))

    def test_show(self):
        test_plot = plots.SubplotFigure()
        with patch('plotly.graph_objects.Figure.show') as show_patch:
            test_plot.show()
            assert show_patch.called


if __name__ == '__main__':
    unittest.main()
