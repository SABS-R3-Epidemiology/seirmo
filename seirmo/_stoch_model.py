
import numpy as np
from _core import SEIRForwardModel, SEIRParameters, SEIRDataCollector
from gillespie import solve_gillespie


class StochasticSEIRModel(SEIRForwardModel):
    def __init__(self, ncompartments, params_names: list):
        super(StochasticSEIRModel, self).__init__()
        self._parameters = SEIRParameters(ncompartments, params_names)
        # sets up n compart and param names output are the variables
        # we want to look at like S, E etc, compartment pops
        self._dataCollector = SEIRDataCollector(['S', 'E', 'I', 'R'])

    def update_propensity(self, current_states: np.ndarray) -> np.ndarray:

        ''' This function takes the current populations in each
        of the N compartments and returns a NxN array where the entry (i,j)
        gives the probabilities that '''

        params_names = self._parameters.parameter_names()
        beta = self._parameters[params_names.index('beta')]
        kappa = self._parameters[params_names.index('kappa')]
        gamma = self._parameters[params_names.index('gamma')]

        [t, S, E, I, R] = current_states
        N = self.n_outputs
        propens_matrix = np.zeros((N,N))
        propens_matrix[0, 1] = beta * S * I
        propens_matrix[1, 2] = kappa * E
        propens_matrix[2, 3] = gamma * I

        return propens_matrix

    def simulate(self, parameters: np.ndarray, times: list):
        self._parameters.configureParameters(parameters)  # array of length 7
        # with values of beta
        # gamma kappa and initial
        self._dataCollector.begin(times)

        initial_states = self._parameters[:4]  # input initial values

        for point in solve_gillespie(
                fun=lambda states: self.update_propensity(states),  # states
                # includes t as first argument
                t_span=[times[0], times[-1]],
                y0=initial_states,
                t_eval=times):
            self._dataCollector.report(point)

        return self._dataCollector.retrieve()
