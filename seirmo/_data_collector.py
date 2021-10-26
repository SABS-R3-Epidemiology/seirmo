"""Module containing the pharmokinetics abstract data collector class.
"""

import numpy as np
from ._core import SEIRDataCollector
import typing


class DataCollector(SEIRDataCollector):
    """Base Data Collecting Class for SEIR Forward Models"""
    def __init__(self, outputNames: typing.List[str]):
        self._output_names = outputNames
        self._n_outputs = len(outputNames)
        self._output_indices = np.arange(self._n_outputs)

    def begin(self, times):
        self._data = np.zeros((len(self._output_names) + 1, len(times)))
        self._data[:, 0] = times
        self._index = 0

    def set_outputs(self, outputs):
        """Sets the Output Parameters to Keep"""
        # Check existence of outputs
        for output in outputs:
            if output not in self._output_names:
                raise ValueError(
                    'The output names specified must be in correct forms')

        output_indices = []
        for output_id, output in enumerate(self._output_names):
            if output in outputs:
                output_indices.append(output_id)

        # Remember outputs
        self._output_indices = output_indices
        self._n_outputs = len(outputs)

    def report(self, data: np.ndarray) -> np.array:
        """Report data as a column vector into an array at each timestep.

        :param data: numpy array containing the data of the model resolution
        :return: numpy array containing the model solution
        """
        assert data.shape == (self.row_width, 1), 'Invalid Data Shape'
        assert self._index < self.column_length, \
               'Too many datapoints reported'
        gill_time = data[0]
        if gill_time > self._data[self._index, 0]:
            self._data[self.__index, 1:] = np.transpose(data[1:])
            self._index += 1

    def reportAll(self, data):
        """Report All Data"""
        # assert data.shape == self._data.shape and
        # self._data[:,0] == data[:, 0]
        self._data = data

    def retrieve_time(self, time_point: float) -> np.ndarray:
        """Return data as a column vector at a time point requested. Asserts
        timepoint is within the 'past' of the model.

        :param time_point: specified time at which we want the data
        :return: data as a column for the specified time step
        :rtype: numpy array column
        """
        assert (
            time_point < self.__index
            and time_point >= 0
            and time_point <= self.column_length
        )
        return np.transpose(self._data[time_point, :])

    def writeToFile(self, filename: str):
        """Opens a given filename and writes data in csv format.

        :param filename: name of the file in which the data will be stored
        """
        with open(filename, "w") as f:
            f.write(",".join(self.column_headers) + '\n')
            for i in range(self.column_length):
                f.write(",".join([str(x) for x in self.__content[i, :]])
                        + '\n')
