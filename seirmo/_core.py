#
# This file is part of seirmo (https://github.com/SABS-R3-Epidemiology/seirmo/)
# which is released under the BSD 3-clause license. See accompanying LICENSE.md
# for copyright notice and full license details.
#


import pints
import typing
import numpy as np


class SEIRParameters():
    """Base Parameter Class for SEIR and Related Forward Models"""
    def __init__(self, nCompartments: int, parameterNames: typing.List[str]):
        self._n_compartments = nCompartments
        self._parameter_names = parameterNames
        self._n_parameters = len(parameterNames)

    def configure_parameters(self, parameters: np.ndarray):
        """Set the current parameters"""
        assert parameters.shape == (self._n_parameters,),\
            f"Expected Parameter Shape {(self._n_parameters,)},\
                but got {parameters.shape}"
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


class SEIROutputCollector():
    """
    Base Class for Accumulating the Output Data from SEIR
    and Related Forward Models
    """
    def __init__(self, outputNames: typing.List[str]):
        self._output_names = outputNames
        self._n_outputs = len(outputNames)
        self._output_indices = np.arange(self._n_outputs)

    def n_outputs(self):
        """Returns the Number of Output Parameters"""
        return self._n_outputs

    def output_names(self):
        """Returns the Names of the Output Parameters"""
        return [self._output_names[x] for x in self._output_indices]

    def set_outputs(self, outputs):
        """Sets the Output Parameters to Keep"""
        # Check existence of outputs
        for output in outputs:
            if output not in self._output_names:
                raise ValueError(
                    'The provided output names are not recognized')

        output_indices = []
        for output_id, output in enumerate(self._output_names):
            if output in outputs:
                output_indices.append(output_id)

        # Remember outputs
        self._output_indices = output_indices
        self._n_outputs = len(outputs)

    def begin(self, *args, **kwargs):
        """
        Abstract method which is called before observations from
        simulation are reported.

        This allows for subclasses to pre-initialize a datastructure
        for when observations are then reported.
        """
        raise NotImplementedError

    def report(self, row):
        """
        Abstract Method which is for reporting observations from
        each iteration of a simulation.

        This allows for subclasses to perform extra operations on the data

        Also allows for subclasses to filter / decide which
        observations should be stored
        """
        raise NotImplementedError

    def report_all(self, data):
        """
        Save all Datapoints to the OutputCollector.

        Overwrites any existing data with this

        : param: data np.ndarray: Data to save.
        """
        self._data = data

    def retrieve(self):
        """
        Returns the Data stored in the Collector.

        If the collector is configured to only output specific columns,
        these are filtered here
        """
        return self._data[:, self._output_indices]


class SEIRForwardModel(pints.ForwardModel):
    """
    Abstract base class for forward SEIR and Related models.

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
            return self._output_collector.n_outputs()
        except AttributeError:
            raise NotImplementedError

    def set_outputs(self, outputs):
        """Set the Desired Output Parameters"""
        try:
            self._output_collector.set_outputs(outputs)
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
            return self._output_collector.output_names()
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
