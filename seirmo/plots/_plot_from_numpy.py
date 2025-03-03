#
# This file is part of seirmo (https://github.com/SABS-R3-Epidemiology/seirmo/)
# which is released under the BSD 3-clause license. See accompanying LICENSE.md
# for copyright notice and full license details.
#

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors


class ConfigurablePlotter:
    """
    A figure class that visualises the population of each compartment over time
    Configurable to plot multiple subplots in one figure, with customised
    labels or colours
    Implements addfill() method to plot a shaded region between two datasets
    (I.e. when plotting confidence intervals)
    """

    def __init__(self):
        pass

    def begin(self, subplots_rows: int = 1, subplots_columns: int = 1):
        """
        Begins creating a figure, with given number of subfigures
        Replaces init class so object can be reused"""
        if not isinstance(subplots_rows, int):
            raise TypeError("Number of rows of subplots must be an integer")
        if not isinstance(subplots_columns, int):
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

        # Ensure self._axes array is always 2D
        if self._nrows == 1 and self._ncolumns == 1:
            self._axes = np.array(self._axes)[np.newaxis, np.newaxis]
        elif self._nrows == 1:
            self._axes = np.array(self._axes)[np.newaxis, :]
        elif self._ncolumns == 1:
            self._axes = np.array(self._axes)[:, np.newaxis]

    def __getitem__(self, index):
        """If figure = ConfigurablePlotter(), then figure.begin().
        Figure[0] will return the matplot figure, and figure[1] will
        return the subplot axis objects"""
        if index == 0:
            return self._fig
        elif index == 1:
            return self._axes
        else:
            raise ValueError("Index must be 0 (for figure) or 1 (for axes)")

    def add_data_to_plot(
        self,
        times: np.ndarray,
        data_array: np.ndarray,
        position: list = [0, 0],
        xlabel: str = "time",
        ylabels: list = [],
        colours: list = [],
        new_axis=False,
    ):
        """Main code to add new data into the plot

        :params:: times: np.ndarray, independent x- variable
        :params:: data_array: np.ndarray, multiple dependent y- variables
                              Data should has one row per timestep,
                              and one column for each dependent variable
        :params:: position: list of integers, gives index of subplot to use
        :params:: xlabel: str
        :params:: ylabel: list of strings (a single string is also accepted)
        :params:: colours: list of valid colour specifiers (ie strings or
                           rgb tuples)
        :params:: new_axis: boolean, set to true if data should
                            be plotted on a second x axis"""

        if len(data_array.shape) == 1:  # Turn any 1D input into 2D
            if (not isinstance(times, np.ndarray) or
                    np.sum(np.shape(times)) == 1):
                # I.e. if only one np.int, or one element array
                times = np.array(times, ndmin=2)
                data_array = data_array[np.newaxis, :]
            else:
                data_array = data_array[:, np.newaxis]

        assert (
            times.shape[0] == data_array.shape[0]
        ), "data and times are not the same length"
        data_width = data_array.shape[1]  # saves the number of y-var

        assert (
            position[0] < self._nrows and position[1] < self._ncolumns
        ), "position and shape are not compatible"

        if new_axis:
            axis = self._axes[position[0], position[1]].twinx()
        else:
            axis = self._axes[position[0], position[1]]

        # Format user inputs
        if len(colours) == 0:  # Default value, if no colous specified
            colours = plt.cm.viridis(np.linspace(0, 1, data_width))
        else:
            colours = matplotlib.colors.to_rgba_array(colours)
        assert data_width == np.shape(colours)[0], \
            'Unexpected number of colours'

        if isinstance(ylabels, str):
            ylabels = [ylabels]  # Converts string input to list
        try:
            iter(ylabels)
        except TypeError:
            raise TypeError('Unexpected type of ylabels')

        # Plot over data array iteratively
        if len(ylabels) > 0:  # If ylabels have been specified for inclusion
            assert data_width == len(ylabels), 'Unexpected number of ylabels'
            for i in range(data_width):
                axis.plot(times, data_array[:, i], color=colours[i],
                          label=ylabels[i])
            axis.legend()
        else:  # Plot without a figure legend
            for i in range(data_width):
                axis.plot(times, data_array[:, i], color=colours[i])

        plt.xlabel(xlabel)
        self._fig.tight_layout()
        return self._fig, self._axes

    def add_fill(
        self,
        times: np.ndarray,
        ymin: np.ndarray,
        ymax: np.ndarray,
        position: list = [0, 0],
        xlabel: str = "time",
        ylabel: str = "number of people",
        colour: str = ["b"],
        alpha: float = 0.2,
    ):
        """Code to plot shaded region between two datasets

        :params:: times: np.ndarray, independent x- variable
        :params:: ymin: np.ndarray, dependent y- variables
        :params:: ymin: np.ndarray, comparison y- variables
        :params:: position: list of integers, gives index of subplot to use
        :params:: xlabel: str
        :params:: ylabel: list of strings
        :params:: colour: any valid colour specifier
        :params:: alpha: float, indicate transparency of filled region

        N.B While it is recommended that y_min should be the (generally)
        smaller dataset for readability, this is not required, and the
        datasets may cross (i.e. y_min may be larger in sections)"""

        assert (
            position[0] < self._nrows and position[1] < self._ncolumns
        ), "position and shape are not compatible"
        axis = self._axes[position[0], position[1]]

        # plots the data
        axis.fill_between(
            times,
            np.squeeze(ymin),
            np.squeeze(ymax),
            color=colour,
            alpha=alpha,
            label=ylabel,
        )
        axis.legend()
        plt.xlabel(xlabel)
        self._fig.tight_layout()
        return self._fig, self._axes

    def show(self):
        plt.show()

    def write_to_file(self, filename: str = "SEIR_stochastic_simulation.pdf"):
        self._fig.savefig(filename)

    def __del__(self):
        if hasattr(self, "_fig"):
            plt.close(self._fig)  # Close figure upon deletion
