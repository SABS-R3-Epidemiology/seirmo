#
# ForwardModel Class
#


class ForwardModel:
    """ForwardModel Class:

    Base class for the model class.

    Parameters
    ----------
    value: numeric, optional
        example of value

    """

    def __init__(self, parameters,times):
        self.parameters = parameters
        self.times = times

    def simulate(self):
        """
        Simulate the daily number of infections for a given time period with given parameters

        Parameters
        ----------
        parameters: sequence of numerics
        times: sequence of numerics

        Returns
        ----------
        n_outputs: numpy array of 1- or 2-dimmension
            array of values of the model at given times
        """
        raise NotImplementedError
