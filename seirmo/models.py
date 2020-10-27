"""#
# This file is part of seirmo (https://github.com/SABS-R3-Epidemiology/seirmo/)
# which is released under the BSD 3-clause license. See accompanying LICENSE.md
# for copyright notice and full license details.
#"""
#
# ForwardModel Class
#


class ForwardModel(object):
    """ForwardModel Class:

    Abstract base class for any models.
    """

    def __init__(self):
        super(ForwardModel, self).__init__()

    def simulate(parameters, times):
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
