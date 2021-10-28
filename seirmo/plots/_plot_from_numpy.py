#
# This file is part of seirmo (https://github.com/SABS-R3-Epidemiology/seirmo/)
# which is released under the BSD 3-clause license. See accompanying LICENSE.md
# for copyright notice and full license details.
#

import numpy as np
import matplotlib.pyplot as plt


class ConfigurablePlotter():
    def __init__(self):
        pass

    def begin(self, subplots_rows: int = 1, subplots_columns: int = 1):
        '''
        Begins creating a figure, with given number of subfigures
        Replaces init class so object can be reused'''
        if type(subplots_rows) != int:
            raise TypeError("Number of rows of subplots must be an integer")
        if type(subplots_columns) != int:
            raise TypeError("Number of columns of subplots must be an integer")
        if subplots_rows <= 0:
            raise ValueError("Number of rows of subplots must be positive")
        if subplots_columns <= 0:
            raise ValueError("Number of columns of subplots must be positive")

        self._fig, self._axes = plt.subplots(subplots_rows, subplots_columns)
        self._size = subplots_columns * subplots_rows
        self._nrows = subplots_rows
        self._ncolumns = subplots_columns
        # we store a figure object and multiple axes objects

    def __getitem__(self, index):
        ''' If figure = ConfigurablePlotter(), then figure.begin().
        Figure[0] will return the matplot figure, and figure[1] will
        return the subplot axis objects'''
        if index == 0:
            return self._fig
        elif index == 1:
            return self._axes
        else:
            raise ValueError("Index must be 0 (for figure) or 1 (for axes)")

    def add_data_to_plot(self, times: np.ndarray, data_array: np.ndarray,
                         position: list = [0, 0],
                         xlabel: str = 'time', ylabels: list = [],
                         colours: list = [], new_axis=False):
        ''' Main code to add new data into the plot
        :params:: times: np.ndarray, independant x- variable
        :params:: data_array: np.ndarray, dependent y- variables
        :params:: position: list of integers, gives index of subplot to use
        :params:: xlabel: str
        :params:: new_axis: boolean, set to true if data should
                            be plotted on a second axis'''

        assert len(times) == data_array.shape[0], \
            'data and times are not the same length'

        if len(data_array.shape) == 1:  # Turn any 1D input into 2D
            if len(times) == 1:
                data_array = data_array[np.newaxis, :]
            else:
                data_array = data_array[:, np.newaxis]

        print(data_array.shape)
        data_width = data_array.shape[1]  # saves the number of y-var


        # if-loop defines which subplot to use,
        # and whether a second axis if needed
        if self._nrows == 1 and self._ncolumns == 1:
            assert position[0] == 0 and position[1] == 0, \
                'position and shape are not compatible'
            if new_axis:
                axis = self._axes.twinx()
            else:
                axis = self._axes

        elif self._ncolumns > 1 and self._nrows == 1:
            assert position[0] < self._nrows \
                and position[1] < self._ncolumns, \
                'position and shape are not compatible'
            if new_axis:
                axis = self._axes[position[1]].twinx()
            else:
                axis = self._axes[position[1]]

        elif self._ncolumns == 1 and self._nrows > 1:
            assert position[0] < self._nrows \
                and position[1] < self._ncolumns, \
                'position and shape are not compatible'
            if new_axis:
                axis = self._axes[position[0]].twinx()
            else:
                axis = self._axes[position[0]]

        else:
            assert position[0] < self._nrows \
                and position[1] < self._ncolumns, \
                'position and shape are not compatible'
            if new_axis:
                axis = self._axes[position[0], position[1]].twinx()
            else:
                axis = self._axes[position[0], position[1]]

        # formats colour choice if none set - I want to change this
        if not colours:
            colours = plt.cm.viridis(np.linspace(0, 1, data_width))

        # plots the data
        for i in range(data_width):
            if i < len(ylabels):
                axis.plot(times, data_array[:, i],
                          color=colours[i], label=ylabels[i])
            else:
                axis.plot(times, data_array[:, i], color=colours[i])
        axis.legend()
        plt.xlabel(xlabel)
        self._fig.tight_layout()
        return self._fig, self._axes

    def add_fill(self, times: np.ndarray, ymin: np.ndarray,
                         ymax: np.ndarray, position: list = [0, 0],
                         xlabel: str = 'time', ylabel: str = 'number of people',
                         colours: str = ['b'], alpha: float = 0.2):
    
        # if-loop defines which subplot to use,
        # and whether a second axis if needed
        if self._nrows == 1 and self._ncolumns == 1:
            assert position[0] == 0 and position[1] == 0, \
                'position and shape are not compatible'
            axis = self._axes

        elif self._ncolumns > 1 and self._nrows == 1:
            assert position[0] < self._nrows \
                and position[1] < self._ncolumns, \
                'position and shape are not compatible'
            axis = self._axes[position[1]]

        elif self._ncolumns == 1 and self._nrows > 1:
            assert position[0] < self._nrows \
                and position[1] < self._ncolumns, \
                'position and shape are not compatible'
            axis = self._axes[position[0]]

        else:
            assert position[0] < self._nrows \
                and position[1] < self._ncolumns, \
                'position and shape are not compatible'
            axis = self._axes[position[0], position[1]]

        # formats colour choice if none set - I want to change this
        if not colours:
            colours = plt.cm.viridis(np.linspace(0, 1, 5))

        # plots the data
        if len(ylabel):
            axis.fill_between(times, ymin, ymax, color=colours[0], alpha = alpha, label=ylabel)
        else:
            axis.fill_between(times, ymin, ymax, color=colours[0], alpha = alpha)
        axis.legend()
        plt.xlabel(xlabel)
        self._fig.tight_layout()
        return self._fig, self._axes
        

    def show(self):
        plt.show()

    def writeToFile(self, filename: str = 'SEIR_stochastic_simulation.png'):
        self._fig.savefig(filename)
