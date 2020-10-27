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
