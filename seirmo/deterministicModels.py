#
# This file is part of seirmo (https://github.com/SABS-R3-Epidemiology/seirmo/)
# which is released under the BSD 3-clause license. See accompanying LICENSE.md
# for copyright notice and full license details.
#

import numpy as np
from scipy.integrate import solve_ivp

import seirmo


class DeterministicSEIRModel(seirmo.SEIRForwardModel):
    r"""
    ODE model: deterministic SEIR
    The SEIR Model has four compartments:
    susceptible individuals (:math:`S`),
    exposed but not yet infectious (:math:`E`),
    infectious (:math:`I`) and recovered (:math:`R`):

    .. math::
        \frac{dS(t)}{dt} = -\beta S(t)I(t),
    .. math::
        \frac{dE(t)}{dt} = \beta S(t)I(t) - \kappa E(t),
    .. math::
        \frac{dI(t)}{dt} = \kappa E(t) - \gamma I(t),
    .. math::
        \frac{dR(t)}{dt} = \gamma I(t),

    where :math:`S(0) = S_0, E(0) = E_0, I(O) = I_0, R(0) = R_0`
    are also parameters of the model.

    Extends :class:`SEIRForwardModel`.
    """

    def __init__(self):
        super(DeterministicSEIRModel, self).__init__()

        # Assign default values
        self._dataCollector = seirmo.SEIRDataCollector(
            ['S', 'E', 'I', 'R', 'Incidence'])
        self._parameters = seirmo.SEIRParameters(
            4, ['S0', 'E0', 'I0', 'R0', 'alpha', 'beta', 'gamma'])

    def _right_hand_side(self, t, y, c):
        # Assuming y = [S, E, I, R] (the dependent variables in the model)
        # Assuming the parameters are ordered like
        # parameters = [S0, E0, I0, R0, beta, kappa, gamma]
        # Let c = [beta, kappa, gamma]
        #  = [parameters[0], parameters[1], parameters[2]],
        # then beta = c[0], kappa = c[1], gamma = c[2]

        # Construct the derivative functions of the system of ODEs

        s, e, i, _ = y
        beta, kappa, gamma = c
        dydt = [-beta * s * i, beta * s * i - kappa * e,
                kappa * e - gamma * i, gamma * i]

        return dydt

    def simulate(self, parameters, times):
        self._parameters.configureParameters(parameters)
        # Define time spans, initial conditions, and constants
        #y_init = parameters[:4]
        #c = parameters[4:]

        # Solve the system of ODEs
        sol = solve_ivp(
            lambda t, y: self._right_hand_side(t, y, self._parameters[4:]),
            [times[0], times[-1]], self._parameters[:4], t_eval=times)

        output = sol['y']

        # Total infected is infectious 'i' plus recovered 'r'
        total_infected = output[2, :] + output[3, :]

        # Number of incidences is the increase in total_infected
        # between the time points (add a 0 at the front to
        # make the length consistent with the solution
        n_incidence = np.zeros(len(times))
        n_incidence[1:] = total_infected[1:] - total_infected[:-1]

        # Append n_incidence to output
        # Output is a matrix with rows being S, E, I, R and Incidence
        output = np.vstack(tup=(output, n_incidence))

        # Get the selected outputs
        self._dataCollector.reportAll(output.transpose())
        #output = output[self._output_indices, :]

        return self._dataCollector.retrieve()
