#
# This file is part of seirmo (https://github.com/SABS-R3-Epidemiology/seirmo/)
# which is released under the BSD 3-clause license. See accompanying LICENSE.md
# for copyright notice and full license details.
#

from scipy.integrate import solve_ivp
from scipy.interpolate import interp1d

import scipy.integrate as integrate


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
    The instantaneous incidence at time :math:`t` is given by:
    .. math::
        \frac{dC(t)}{dt} = \kappa E(t),
    and the weekly incidence will be given by its integral.
    """

    def __init__(self):
        super(SEIRModel, self).__init__()

    def _right_hand_side(self, t, y, c):
        # Assuming y = [S, E, I, R, C] (the dependent variables in the model)
        # Assuming the parameters are ordered like
        # parameters = [S0, E0, I0, R0, C0, beta, kappa, gamma]
        # Let c = [beta, kappa, gamma]
        #  = [parameters[0], parameters[1], parameters[2]],
        # then beta = c[0], kappa = c[1], gamma = c[2]

        # Construct the derivative functions of the system of ODEs

        s, e, i, _, _ = y
        beta, kappa, gamma = c
        dydt = [-beta * s * i, beta * s * i - kappa * e,
                kappa * e - gamma * i, gamma * i, kappa * e]

        return dydt

    # Return the number of new cases between provided times
    def _compute_incidences(self, n_incidence, times, t_i, t_f):
        n_incidence_interp = interp1d(times, n_incidence, kind='cubic')
        return integrate.quad(n_incidence_interp, t_i, t_f)

    def simulate(self, parameters, times, t_i, t_f, return_incidence=False):

        # Define time spans, initial conditions, and constants
        y_init = parameters[0:5]
        c = parameters[5:]

        # Solve the system of ODEs
        sol = solve_ivp(lambda t, y: self._right_hand_side(t, y, c),
                        [times[0], times[-1]], y_init, t_eval=times)

        if return_incidence is False:
            return sol['y'][0:4, :].transpose()
        elif return_incidence is True:
            n_incidence = sol['y'][4:, :]
            return self._compute_incidences(n_incidence, times, t_i, t_f)
