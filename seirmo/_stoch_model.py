#
# This file is part of seirmo (https://github.com/SABS-R3-Epidemiology/seirmo/)
# which is released under the BSD 3-clause license. See accompanying LICENSE.md
# for copyright notice and full license details.
#

import numpy as np
import seirmo as se
from ._gillespie import solve_gillespie


class StochasticSEIRModel(se.SEIRForwardModel):
    r"""
    ODE model: Stochastic SEIR
    The SEIR Model has four compartments:
    susceptible individuals (:math:`S`),
    exposed but not yet infectious (:math:`E`),
    infectious (:math:`I`) and recovered (:math:`R`):

    Possible processes between compartments:

    Exposure: S -> E, at rate :math:\beta S(t)I(t)``
    Infection: E -> I, at rate :math:\kappa E(t)``
    Recovery: I -> R, at rate :math:\gamma I(t)``

    Can be used in conjunction with solve_gillespie(),
    a stochastic ODE solver implemented in this package.

    Extends :class:`SEIRForwardModel`.
    """
    def __init__(self, params_names: list):
        super(StochasticSEIRModel, self).__init__()
        self._parameters = se.SEIRParameters(params_names)
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
        N = len(current_states) - 1
        propens_matrix = np.zeros((N, N))
        propens_matrix[0, 1] = beta * S * I
        propens_matrix[1, 2] = kappa * E
        propens_matrix[2, 3] = gamma * I

        return propens_matrix

    def simulate(self, parameters: np.ndarray, times: list,
                 max_t_step: float = 0.01):
        self._parameters.configure_parameters(parameters)  # array of length 7
        # with values of beta
        # gamma kappa and initial
        self._output_collector.begin(times)

        initial_states = self._parameters[:4]  # input initial values

        for point in solve_gillespie(
                lambda states: self.update_propensity(states),  # states
                # includes t as first argument
                initial_states,
                [times[0], times[-1]], max_t_step):

            self._output_collector.report(point)
            self._output_collector.retrieve()

        return self._output_collector.retrieve()
