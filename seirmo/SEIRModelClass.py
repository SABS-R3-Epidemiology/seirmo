"""#
# This file is part of seirmo (https://github.com/SABS-R3-Epidemiology/seirmo/)
# which is released under the BSD 3-clause license. See accompanying LICENSE.md
# for copyright notice and full license details.
#"""
from scipy.integrate import solve_ivp
import ForwardModel


class SEIRModel(ForwardModel):
    """
    To be added
    """

    def __init__(self):
        super(SEIRModel, self).__init__()

    def simulate(self, parameters, times):

        # Assuming y = [S, E, I, R] (the dependent variables in the model)
        # Assuming the parameters are ordered like
        # parameters = [beta, kappa, gamma, S0, E0, I0, R0]
        # Let c = [beta, kappa, gamma]
        #  = [parameters[0], parameters[1], parameters[2]],
        # then beta = c[0], kappa = c[1], gamma = c[2]

        # Construct the derivative functions of the system of ODEs
        def f(t, y, c):
            dydt = [-c[0] * y[0] * y[2], c[0] * y[0] * y[2] - c[1] * y[1],
                    c[1] * y[1] - c[2] * y[2], c[2] * y[2]]
            return dydt

        # Define time spans, initial conditions, and constants
        t_span = times
        y_init = parameters[3:]
        c = parameters[0:3]

        # Solve the system of ODEs
        sol = solve_ivp(lambda t, y: f(t, y, c),
                        [t_span[0], t_span[-1]], y_init, t_eval=t_span)

        return sol
