#
# This file is part of seirmo (https://github.com/SABS-R3-Epidemiology/seirmo/)
# which is released under the BSD 3-clause license. See accompanying LICENSE.md
# for copyright notice and full license details.
#

import numpy as np

import seirmo as se


class SimulationController(object):
    """SimulationController Class:

    Runs the simulation of any model and controls outputs

    Parameters
    ----------
    model: seirmo.ForwardModel class
    start: simulation start time
    end: simulation end time
    """

    def __init__(self, model, start, end, n_times): # noqa
        super(SimulationController, self).__init__()

        if not isinstance(model, se.ForwardModel):
            raise TypeError(
                'Model has to be an instance of seirmo.ForwardModel.')

        self._model = model
        self._simulation_times = np.linspace(start, end, n_times)

    def run(self, parameters):

        return self._model.simulate(parameters, self._simulation_times)
