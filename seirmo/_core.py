#
# This file is part of seirmo (https://github.com/SABS-R3-Epidemiology/seirmo/)
# which is released under the BSD 3-clause license. See accompanying LICENSE.md
# for copyright notice and full license details.
#


import pints
import typing
import numpy as np


class SEIRParameters():
    """Base Parameter Class for SEIR Forward Models"""
    def __init__(self, nCompartments: int, parameterNames: typing.List[str]):
        self._n_compartments = nCompartments
        self._parameter_names = parameterNames
        self._n_parameters = len(parameterNames)

    def configureParameters(self, parameters: np.ndarray):
        """Set the current parameters"""
        assert parameters.shape == (self._n_parameters,),\
            f"Expected Parameter Shape {(self._n_parameters,)}, but got {parameters.shape}"
        self._parameters = parameters

    def n_parameters(self):
        """Returns the Number of Model Parameters"""
        return self._n_parameters

    def parameter_names(self):
        """Returns the Names of the Model Parameters"""
        return self._parameter_names

    def __getitem__(self, val):
        """Retrieve Parameters"""
        return self._parameters[val]


class SEIRDataCollector():
    """Base Data Collecting Class for SEIR Forward Models"""
    def __init__(self, outputNames: typing.List[str]):
        self._output_names = outputNames
        self._n_outputs = len(outputNames)
        self._output_indices = np.arange(self._n_outputs)

    def n_outputs(self):
        """Returns the Number of Output Parameters"""
        return self._n_outputs

    def output_names(self):
        """Returns the Name of the Output Parameters"""
        return [self._output_names[x] for x in self._output_indices]

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

    def report(self, row):
        """Report a Single Datapoint"""
        pass

    def reportAll(self, data):
        """Report All Data"""
        # Perform some check
        self._data = data

    def retrieve(self):
        """Return Formatted Data"""
        return self._data[:, self._output_indices]


class SEIRForwardModel(pints.ForwardModel):
    """
    Abstract base class for forward seir models.

    Extends :class:`pints.ForwardModel`.
    """
    def __init__(self):
        super(SEIRForwardModel, self).__init__()

    def n_parameters(self):
        """Returns Number of Model parameters"""
        try:
            return self._parameters.n_parameters()
        except AttributeError:
            raise NotImplementedError

    def n_outputs(self):
        """Returns Number of Output Parameters"""
        try:
            return self._dataCollector.n_outputs()
        except AttributeError:
            raise NotImplementedError

    def set_outputs(self, outputs):
        """Set the Desired Output Parameters"""
        try:
            self._dataCollector.set_outputs(outputs)
        except AttributeError:
            raise NotImplementedError

    def parameter_names(self):
        """Returns the Model Parameter Names"""
        try:
            return self._parameters.parameter_names()
        except AttributeError:
            raise NotImplementedError

    def output_names(self):
        """Returns the Output Names"""
        try:
            return self._dataCollector.output_names()
        except AttributeError:
            raise NotImplementedError

    def simulate(self, parameters, times):
        """
        Forward simulation of a model for a given time period
        with given parameters
        Returns a sequence of length ``n_times`` (for single output problems)
        or a NumPy array of shape ``(n_times, n_outputs)`` (for multi-output
        problems), representing the values of the model at the given ``times``.

        :param parameters: An array-like object with parameter values of length
            :meth:`n_parameters`.
        :type parameters: list | numpy.ndarray
        :param times: An array-like object with time points.
        :type times: list | numpy.ndarray
        """
        raise NotImplementedError
