#
# This file is part of seirmo (https://github.com/SABS-R3-Epidemiology/seirmo/)
# which is released under the BSD 3-clause license. See accompanying LICENSE.md
# for copyright notice and full license details.
#

import unittest
import numpy as np
import matplotlib
from parameterized import parameterized
from unittest import mock

import seirmo as se


numReps = 10


class TestPlotFromNumpy(unittest.TestCase):
    """
    Test the 'ConfigurablePlotter' class.
    """

    @parameterized.expand([(np.random.randint(1, 5, (2,)),)
                           for _ in range(numReps)])
    def test_begin(self, plot_num):
        row_num, col_num = plot_num
        figure = se.plots.ConfigurablePlotter()
        figure.begin(int(row_num), int(col_num))
        self.assertEqual(figure._nrows, row_num,
                         'Unexpected number of subplot rows')
        self.assertEqual(figure._ncolumns, col_num,
                         'Unexpected number of subplot columns')
        self.assertEqual(figure._size, int(row_num * col_num),
                         'Unexpected number of subplots')
        self.assertEqual(np.product(np.shape(figure._axes)),
                         int(row_num * col_num),
                         'Unexpected number of axes objects')

    @parameterized.expand([(1, 1), (3, 1), (1, 3), (3, 3)])
    def test_begin_axes_objects(self, row_num, col_num):
        figure = se.plots.ConfigurablePlotter()
        figure.begin(int(row_num), int(col_num))
        self.assertEqual(np.shape(figure._axes),
                         (row_num, col_num),
                         'Unexpected shape of axes objects')

    def test_begin_bad_input(self):
        figure = se.plots.ConfigurablePlotter()
        with self.assertRaises(ValueError):
            figure.begin(0, 1)
        with self.assertRaises(ValueError):
            figure.begin(1, -1)
        with self.assertRaises(TypeError):
            figure.begin(1.5, 2)
        with self.assertRaises(TypeError):
            figure.begin(1, 'five')

    def test_indexing(self):
        figure = se.plots.ConfigurablePlotter()
        figure.begin(2, 2)
        self.assertEqual(type(figure[0]), matplotlib.figure.Figure,
                         "Unable to retrieve figure object via indexing")
        self.assertTrue(isinstance(figure[1][0, 0], matplotlib.axes.Axes))
        with self.assertRaises(ValueError):
            figure[2]  # Should be out of indexing range - handled in file

    def test_add_data_assertions(self):
        figure = se.plots.ConfigurablePlotter()
        figure.begin(2, 2)
        times = np.array([0, 1, 2, 3, 4])
        data_array = np.arange(20).reshape(5, 4)
        with self.assertRaises(AssertionError):
            figure.add_data_to_plot(times[1:], data_array)
        with self.assertRaises(AssertionError):
            figure.add_data_to_plot(times, data_array, position=[3, 1])

    def test_add_data_function(self):
        figure = se.plots.ConfigurablePlotter()
        figure.begin(1, 2)
        times = np.array([0, 1, 2, 3, 4])
        data_array = np.arange(5).reshape(5, 1)
        figure.add_data_to_plot(times, data_array,
                                position=[0, 0], ylabels='label')
        self.assertAlmostEqual(figure[1][0, 0].lines[0].get_color().tolist(),
                               [0.267004, 0.004874, 0.329415, 1.],
                               'Unexpected colour in axes object')
        #  The test above is based on the viridis default
        figure.add_data_to_plot(times, data_array + 1, position=[0, 1],
                                colours=['#a3c1ad'])
        self.assertEqual(figure[1][0, 1].lines[0].get_color(), '#a3c1ad',
                         'Unexpected colour in axes object')

        figure.add_data_to_plot(times[0], data_array[0, :])
        figure.add_data_to_plot(times, data_array[:, 0])
        # These must both pass without error to verify 1D data can be passed

    def test_add_data_new_axis(self):
        def has_twinx(ax):
            s = ax.get_shared_x_axes().get_siblings(ax)
            if len(s) > 1:
                for ax1 in [ax1 for ax1 in s if ax1 is not ax]:
                    if ax1.bbox.bounds == ax.bbox.bounds:
                        return True
            return False

        figure = se.plots.ConfigurablePlotter()
        figure.begin(1, 3)
        times = np.array([0, 1, 2, 3, 4])
        data_array = np.arange(20).reshape(5, 4)
        figure.add_data_to_plot(times, data_array, position=[0, 0])
        figure.add_data_to_plot(times, data_array + 2,
                                position=[0, 1], new_axis=False)
        figure.add_data_to_plot(times, data_array + 4,
                                position=[0, 1], new_axis=True)

        self.assertTrue(has_twinx(figure._axes[0, 1]))
        self.assertFalse(has_twinx(figure._axes[0, 2]))

    def test_add_fill_assertions(self):
        figure = se.plots.ConfigurablePlotter()
        figure.begin(2, 2)
        times = np.array([0, 1, 2, 3, 4])
        data_array = np.arange(20).reshape(5, 4)
        data_array2 = np.arange(20).reshape(5, 4) + 2
        with self.assertRaises(AssertionError):
            figure.add_data_to_plot(times[1:], data_array)
        with self.assertRaises(AssertionError):
            figure.add_fill(times, data_array, data_array2, position=[3, 1])

    def test_add_fill_function(self):
        figure = se.plots.ConfigurablePlotter()
        figure.begin(1, 2)
        times = np.array([0, 1, 2, 3, 4])
        data_array = np.arange(5).reshape(5, 1)
        figure.add_fill(times, data_array, data_array * 2,
                        position=[0, 0], ylabel='label')
        colour = np.squeeze(figure[1][0, 0].collections[0].get_facecolor())
        self.assertAlmostEqual(colour.tolist(), [0.0, 0.0, 1.0, 0.2],
                               'Unexpected colour in axes object')
        #  The test above is based on the blue default in function definition
        figure.add_fill(times, data_array, data_array * 2,
                        position=[0, 1], colours='r')
        colour_red = np.squeeze(figure[1][0, 1].collections[0].get_facecolor())
        self.assertAlmostEqual(colour_red.tolist(), [1, 0, 0, 0.2],
                               'Unexpected colour in axes object')

    @mock.patch("seirmo.plots._plot_from_numpy.plt")
    def test_plot_data(self, mock_pyplot):
        figure = se.plots.ConfigurablePlotter()
        figure.show()
        mock_pyplot.show.assert_called_once()

    # @mock.patch("seirmo.plots.ConfigurablePlotter")
    # def test_save_data2(self, mock_class):
    #     figure = mock_class()
    #     figure.writeToFile()
    #     mock_class._fig.savefig.assert_called_once()
    #     # THIS IS CURRENTLY FAILING


class TestStochasticSimPlotter(unittest.TestCase):
    """
    Test the 'StochasticPlotter' class.
    """

    def test_init_method(self):
        times = np.array([0, 1, 2, 3, 4])
        data = np.arange(5).reshape(5, 1) + 1
        figure = se.plots.StochasticPlotter(times, data)
        self.assertEqual(np.squeeze(figure._data).tolist(),
                         [1, 2, 3, 4, 5, ],
                         'Stored data not equal to input data')
        self.assertEqual(figure._times.tolist(), [0, 1, 2, 3, 4],
                         'Stored times not equal to input times')

    @mock.patch("seirmo.plots._stochastic_sim_plotter.plt.show")
    def test_plot_method(self, mock_show):
        times = np.array([0, 1, 2, 3, 4])
        data = np.arange(25).reshape(5, 5)
        figure = se.plots.StochasticPlotter(times, data)
        figure.plot(labels=['a', 'b', 'c', 'd'])
        mock_show.assert_called_once()


if __name__ == '__main__':
    unittest.main()
    matplotlib.pyplot.close('all')  # Is this also useful here?
