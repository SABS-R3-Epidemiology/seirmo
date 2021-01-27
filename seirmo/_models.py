#
# This file is part of seirmo (https://github.com/SABS-R3-Epidemiology/seirmo/)
# which is released under the BSD 3-clause license. See accompanying LICENSE.md
# for copyright notice and full license details.
#

import numpy as np
from scipy.integrate import solve_ivp


class SEIRModel(pints.ForwardModel):
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
    """

    def __init__(self):
        super(SEIRModel, self).__init__()

        # Assign default values
        self.output_names = ['S', 'E', 'I', 'R', 'Incidence']
        # The default number of outputs is 5,
        # i.e. S, E, I, R and Incidence
        self.n_outputs = 5
        # The default number of outputs is 7,
        # i.e. 4 initial conditions and 3 parameters
        self.n_parameters = 7

    def n_outputs(self):
        # Return the number of outputs
        return self.n_outputs
    
    def n_parameters(self):
        # Return the number of parameters
        return self.n_parameters

    def set_outputs(self, outputs=['Incidence']):
        self.output_names = outputs
        self.n_outputs = len(outputs)

    def output_names(self):
        # Return the (selected) output names
        return self.output_names

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

        # Define time spans, initial conditions, and constants
        y_init = parameters[:4]
        c = parameters[4:]

        # Solve the system of ODEs
        sol = solve_ivp(lambda t, y: self._right_hand_side(t, y, c),
                        [times[0], times[-1]], y_init, t_eval=times)

        output = sol['y']

        # Total infected is infectious 'i' plus recovered 'r'
        total_infected = output[2, :] + output[3, :]

        # Number of incidences is the increase in total_infected
        # between the time points (add a 0 at the front to
        # make the length consistent with the solution
        n_incidence = np.zeros(len(times))
        n_incidence[1:] = total_infected[1:] - total_infected[:-1]

        # Append n_incidence to output
        output = np.vstack(tup=(output, n_incidence))
        return output.transpose()
