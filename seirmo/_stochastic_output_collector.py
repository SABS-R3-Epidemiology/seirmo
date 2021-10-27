


import numpy as np
import seirmo as se
import typing


class StochasticOutputCollector(se.SEIROutputCollector):
    '''    """Base Data Collecting Class for SEIR Forward Models"""
    def __init__(self, outputNames: typing.List[str]):
        self._output_names = outputNames
        self._n_outputs = len(outputNames)
        self._output_indices = np.arange(self._n_outputs)
    '''
    def begin(self, times):
        self._data = np.zeros((len(times), len(self._output_names) + 1))
        self._data[:, 0] = times
        self._index = 0

    '''def set_outputs(self, outputs):
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
        self._n_outputs = len(outputs)'''

    def report(self, data: np.ndarray) -> np.array:
        """Report data as a column vector into an array at each timestep.

        :param data: numpy array containing the data of the model resolution
        :return: numpy array containing the model solution
        """
        if self._index >= self._data.shape[0]:
            return
        assert data.shape == (self._data.shape[1],), 'Invalid Data Shape'
        
        gill_time = data[0]
        if gill_time > self._data[self._index, 0]:
            self._data[self._index, 1:] = np.transpose(data[1:])
            self._index += 1

    '''def reportAll(self, data):
        """Report All Data"""
        # assert data.shape == self._data.shape and
        # self._data[:,0] == data[:, 0]
        self._data = data
'''
    def retrieve_time(self, index:int) -> np.ndarray:
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
