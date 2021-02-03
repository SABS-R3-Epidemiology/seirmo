#
# This file is part of seirmo (https://github.com/SABS-R3-Epidemiology/seirmo/)
# which is released under the BSD 3-clause license. See accompanying LICENSE.md
# for copyright notice and full license details.
#

import copy

import numpy as np
import pints
from scipy.integrate import solve_ivp


class ForwardModel(pints.ForwardModel):
    """
    Abstract base class for forward models.

    Extends :class:`pints.ForwardModel`.
    """
    def __init__(self):
        super(ForwardModel, self).__init__()

    def n_outputs(self):
        """
        Returns the number of model outputs.
        """
        raise NotImplementedError

    def n_parameters(self):
        """
        Returns the number of model parameters.
        """
        raise NotImplementedError

    def output_names(self):
        """
        Returns the names of the model outputs.
        """
        raise NotImplementedError

    def parameter_names(self):
        """
        Returns the names of the model parameters.
        """
        raise NotImplementedError

    def set_outputs(self, outputs):
        """
        Sets the outputs of the model.
        """
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

    Extends :class:`ForwardModel`.
    """

    def __init__(self):
        super(SEIRModel, self).__init__()

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

    def simulate(self, parameters, times, return_incidence=False):

        # Define time spans, initial conditions, and constants
        y_init = parameters[:4]
        c = parameters[4:]

        # Solve the system of ODEs
        sol = solve_ivp(lambda t, y: self._right_hand_side(t, y, c),
                        [times[0], times[-1]], y_init, t_eval=times)

        output = sol['y']

        if not return_incidence:
            return output.transpose()

        # Total infected is infectiout 'i' plus recovered 'r'
        total_infected = output[2, :] + output[3, :]

        # Number of incidences is the increase in total_infected
        # between the time points (add a 0 at the front to
        # make the length consistent with the solution
        n_incidence = np.zeros(len(times))
        n_incidence[1:] = total_infected[1:] - total_infected[:-1]

        # Append n_incidence to output
        output = np.vstack(tup=(output, n_incidence))
        return output.transpose()


class ReducedModel(ForwardModel):
    """
    A class that can be used to permanently fix model parameters of a
    :class:`ForwardModel` instance.

    This may be useful to explore simplified versions of a model without
    reimplementing the model itself.

    Extends :class:`ForwardModel`.

    :param model: An instance of a :class:`ForwardModel`.
    :type model: ForwardModel
    """
    def __init__(self, model):
        super(ReducedModel, self).__init__()

        # Check input
        if not isinstance(model, ForwardModel):
            raise TypeError(
                'The model has to be an instance of a seirmo.ForwardModel.')

        self._model = model

        # Set defaults
        self._fixed_params_mask = None
        self._fixed_params_values = None
        self._n_parameters = model.n_parameters()
        self._parameter_names = model.parameter_names()

    def fix_parameters(self, name_value_dict):
        """
        Fixes the value of model parameters, and effectively removes them as a
        parameter from the model. Fixing the value of a parameter at ``None``,
        sets the parameter free again.

        :param name_value_dict: A dictionary with model parameter names as
            keys, and parameter values as values.
        :type name_value_dict: dict
        """
        # Check type
        try:
            name_value_dict = dict(name_value_dict)
        except (TypeError, ValueError):
            raise ValueError(
                'The name-value dictionary has to be convertable to a python '
                'dictionary.')

        # If no model parameters have been fixed before, instantiate a mask
        # and values
        if self._fixed_params_mask is None:
            self._fixed_params_mask = np.zeros(
                shape=self._n_parameters, dtype=bool)

        if self._fixed_params_values is None:
            self._fixed_params_values = np.empty(shape=self._n_parameters)

        # Update the mask and values
        for index, name in enumerate(self._parameter_names):
            try:
                value = name_value_dict[name]
            except KeyError:
                # KeyError indicates that parameter name is not being fixed
                continue

            # Fix parameter if value is not None, else unfix it
            self._fixed_params_mask[index] = value is not None
            self._fixed_params_values[index] = value

        # If all parameters are free, set mask and values to None again
        if np.alltrue(~self._fixed_params_mask):
            self._fixed_params_mask = None
            self._fixed_params_values = None

    def n_fixed_parameters(self):
        """
        Returns the number of fixed model parameters.
        """
        if self._fixed_params_mask is None:
            return 0

        n_fixed = int(np.sum(self._fixed_params_mask))

        return n_fixed

    def n_outputs(self):
        """
        Returns the number of model outputs.
        """
        return self._model.n_outputs()

    def n_parameters(self):
        """
        Returns the number of model parameters.
        """
        # Get number of fixed parameters
        n_fixed = 0
        if self._fixed_params_mask is not None:
            n_fixed = int(np.sum(self._fixed_params_mask))

        # Subtract fixed parameters from total number
        n_parameters = self._n_parameters - n_fixed

        return n_parameters

    def output_names(self):
        """
        Returns the names of the model outputs.
        """
        return self._model.output_names()

    def parameter_names(self):
        """
        Returns the names of the model parameters.
        """
        # Remove fixed model parameters
        names = self._parameter_names
        if self._fixed_params_mask is not None:
            names = np.array(names)
            names = names[~self._fixed_params_mask]
            names = list(names)

        return copy.copy(names)

    def set_outputs(self, outputs):
        """
        Sets the outputs of the model.
        """
        self._model.set_outputs(outputs)

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
        # Insert fixed parameter values
        if self._fixed_params_mask is not None:
            self._fixed_params_values[
                ~self._fixed_params_mask] = parameters
            parameters = self._fixed_params_values

        return self._model.simulate(parameters, times)
