#
# This file is part of seirmo (https://github.com/SABS-R3-Epidemiology/seirmo/)
# which is released under the BSD 3-clause license. See accompanying LICENSE.md
# for copyright notice and full license details.
#

import numpy as np
import seirmo as se
from ._gillespie import solve_gillespie


class StochasticSEIRModel(se.SEIRForwardModel):
    def __init__(self, ncompartments, params_names: list):
        super(StochasticSEIRModel, self).__init__()
        self._parameters = se.SEIRParameters(ncompartments, params_names)
        # sets up n compart and param names output are the variables
        # we want to look at like S, E etc, compartment pops
        self._output_collector = se.StochasticOutputCollector(
            ['S', 'E', 'I', 'R'])

    def update_propensity(self, current_states: np.ndarray) -> np.ndarray:

        ''' This function takes the current populations in each
        of the N compartments and returns a NxN array where the entry (i,j)
        gives the probabilities that '''

        params_names = self._parameters.parameter_names()
        beta = self._parameters[params_names.index('beta')]
        kappa = self._parameters[params_names.index('kappa')]
        gamma = self._parameters[params_names.index('gamma')]

        [t, S, E, I, R] = current_states
        N = self._parameters._n_compartments
        propens_matrix = np.zeros((N, N))
        propens_matrix[0, 1] = beta * S * I
        propens_matrix[1, 2] = kappa * E
        propens_matrix[2, 3] = gamma * I

        return propens_matrix

    def simulate(self, parameters: np.ndarray, times: list):
        self._parameters.configure_parameters(parameters)  # array of length 7
        # with values of beta
        # gamma kappa and initial
        self._output_collector.begin(times)

        initial_states = self._parameters[:4]  # input initial values

        for point in solve_gillespie(
                fun=lambda states: self.update_propensity(states),  # states
                # includes t as first argument
                y0=initial_states,
                t_span=[times[0], times[-1]]):
            self._output_collector.report(point)

        return self._output_collector.retrieve()
