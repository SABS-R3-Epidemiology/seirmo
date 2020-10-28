#
# This file is part of seirmo (https://github.com/SABS-R3-Epidemiology/seirmo/)
# which is released under the BSD 3-clause license. See accompanying LICENSE.md
# for copyright notice and full license details.
#

from scipy.integrate import solve_ivp


class ForwardModel(object):
    """ForwardModel Class:

    Abstract base class for any models.
    """

    def __init__(self):
        super(ForwardModel, self).__init__()

    def simulate(self, parameters, times):
        """
        Forward simulation of a model for a given time period
        with given parameters

        Returns a sequence of length ``n_times`` (for single output problems)
        or a NumPy array of shape ``(n_times, n_outputs)`` (for multi-output
        problems), representing the values of the model at the given ``times``.

        Parameters
        ----------
        parameters: sequence of numerics
        times: sequence of numerics
        """
        raise NotImplementedError


class SEIRModel(ForwardModel):
    """
    To be added
    """

    def __init__(self):
        super(SEIRModel, self).__init__()

    def _right_hand_side(self):
        # Assuming y = [S, E, I, R] (the dependent variables in the model)
        # Assuming the parameters are ordered like
        # parameters = [beta, kappa, gamma, S0, E0, I0, R0]
        # Let c = [beta, kappa, gamma]
        #  = [parameters[0], parameters[1], parameters[2]],
        # then beta = c[0], kappa = c[1], gamma = c[2]

        # Construct the derivative functions of the system of ODEs
        def f(t, y, c):
            S, E, I, R = y
            beta, kappa, gamma = c
            dydt = [-beta * S * I, beta * S * I - kappa * E,
                    kappa * E - gamma * I, gamma * I]
            return dydt

        return f

    def simulate(self, parameters, times):

        # Define time spans, initial conditions, and constants
        y_init = parameters[3:]
        c = parameters[0:3]

        # Solve the system of ODEs
        sol = solve_ivp(lambda t, y: self._right_hand_side(t, y, c),
                        [times[0], times[-1]], y_init, t_eval=times)

        return sol['y'].transpose()

