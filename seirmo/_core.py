#
# This file is part of seirmo (https://github.com/SABS-R3-Epidemiology/seirmo/)
# which is released under the BSD 3-clause license. See accompanying LICENSE.md
# for copyright notice and full license details.
#


import pints
import typing
import numpy as np


class SEIRParameters:
    def __init__(self, nCompartments: int, parameterNames: typing.List[str]):
        self._numCompartments = nCompartments
        self._parameterNames = parameterNames
        self._nParameters = len(parameterNames)

    def configureParameters(self, parameters: np.ndarray):
        self._parameters = parameters

    def n_parameters(self):
        return self._nParameters

    def parameter_names(self):
        return self._parameterNames

    def __getitem__(self, val):
        return self._parameters[val]


class SEIRDataCollector:
    def __init__(self, outputNames: typing.List[str]):
        self._outputNames = outputNames
        self._nOutputs = len(outputNames)

    def n_outputs(self):
        return self._nOutputs

    def output_names(self):
        return self._outputNames


class SEIRForwardModel(pints.ForwardModel):
    def __init__(self):
        raise NotImplementedError

    def n_parameters(self):
        return self._parameters.n_parameters()

    def n_outputs(self):
        return self._dataCollector.n_outputs()

    def set_outputs(self, outputs):
        raise NotImplemented

    def parameter_names(self):
        return self._parameters.parameter_names()

    def output_names(self):
        return self._outputs.output_names()

    def simulate(self, parameters, times):
        raise NotImplementedError


"""
class DemoModel(SEIRForwardModel):
    def __init__(self):
        self._parameters = SEIRParameters(4, ['S0', 'E0', 'I0', 'R0', 'alpha', 'beta', 'gamma'])
        self._dataCollector = SEIRDataCollector(['S', 'E', 'I', 'R', 'Incidence'])

    def simulate(self, parameters, times):
        'Do stuff'
"""
