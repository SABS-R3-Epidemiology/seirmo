#
# ForwardModel Class
#


class ForwardModel(object):
    """ForwardModel Class:

    Abstract base class for any models.

    """

    def __init__(self):
        super(ForwardModel, self).__init__()

    def simulate(self):
        """
        Forward simulation of a model for a given time period with given parameters

        Parameters
        ----------
        parameters: sequence of numerics
        times: sequence of numerics

        Returns
        ----------
        output: numpy array of 1- or 2-dimension
            Array of values of the model at given times.
            Returns sequence of length times for single output problem
            Returns NumPy array of shape (times,outputs) for multi-outputs problem

        """
        raise NotImplementedError
