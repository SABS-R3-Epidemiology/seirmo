#
# This file is part of seirmo (https://github.com/SABS-R3-Epidemiology/seirmo/)
# which is released under the BSD 3-clause license. See accompanying LICENSE.md
# for copyright notice and full license details.
#

import models


class SimulationController(ForwardModel):
    """SimulationController Class:

    Runs the simulation of any model
    """

    def __init__(self, start_simulation_time: float, end_simulation_time: float): # noqa
        super(SimulationController, self).__init__()
        self.simulation_times = (start_simulation_time, end_simulation_time)

    def run(self, parameters):

        output = ForwardModel.simulate(parameters, self.simulation_times)

        return output
