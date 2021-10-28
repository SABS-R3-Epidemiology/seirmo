#
# This file is part of seirmo (https://github.com/SABS-R3-Epidemiology/seirmo/)
# which is released under the BSD 3-clause license. See accompanying LICENSE.md
# for copyright notice and full license details.
#

import numpy as np
import seirmo as se
# import typing


class StochasticOutputCollector(se.SEIROutputCollector):
    def begin(self, times):
        self._data = np.full((len(times), len(self._output_names)), np.nan)
        self._index = 0
        self._times = np.array(times)

    def report(self, data: np.ndarray) -> np.array:
        """Report data as a column vector into an array at each timestep.

        :param data: numpy array containing the data of the model resolution
        :return: numpy array containing the model solution
        """
        if self._index >= self._data.shape[0]:
            return
        assert data.shape == (self._data.shape[1] + 1,), 'Invalid Data Shape'
        gill_time = data[0]
        if gill_time >= self._times[self._index]:
            self._data[self._index, :] = np.transpose(data[1:])
            self._index += 1

    def retrieve_time(self, index: int) -> np.ndarray:
        """Return data as a column vector at a time point requested. Asserts
        timepoint is within the 'past' of the model.

        :param time_point: specified time at which we want the data
        :return: data as a column for the specified time step
        :rtype: numpy array column
        """

        assert (
            index < self._index
            and index >= 0
            and index < self._data.shape[0]
        )
        return np.transpose(self._data[index, :])
