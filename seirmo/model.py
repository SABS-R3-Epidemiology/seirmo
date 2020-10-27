#
# ForwardModel Class
#


class ForwardModel:
    """ForwardModel Class:

    Abstract base class for the SEIR model class.

    Parameters
    ----------
    value: numeric, optional
        example of value

    """

    def __init__(self):

    def simulate(self):
        """
        Forward simulate the daily number of infections for a given time period with given parameters

        Parameters
        ----------
        parameters: sequence of numerics
        times: sequence of numerics

        Returns
        ----------
        n_outputs: numpy array of 1- or 2-dimmension
            Array of values of the model at given times.
            Returns sequence of length times for single output problem
            Returns NumPy array of shape (times,outputs) for multi-outputs problem

        """
        raise NotImplementedError
