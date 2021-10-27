#
# This file is part of seirmo (https://github.com/SABS-R3-Epidemiology/seirmo/)
# which is released under the BSD 3-clause license. See accompanying LICENSE.md
# for copyright notice and full license details.
#

import numpy as np
import typing


def solve_gillespie(propensities: typing.Callable[[np.ndarray], np.ndarray],
                    initial_cond: np.ndarray, t_span: typing.List[float],
                    max_t_step: float = 0.01):
    """ Solve an initial_cond value problem using gillespie algorithm

    This function numerically integrates a system of ordinary differential
    equations given initial_cond conditions. We use the Gillespie algorithm
    with tau-leaping, so that the time step is not uniform but sampled randomly

    N.B If all propensities are zero, this would give an infinite timestep.
    We allow the simulation to continue at a large time_step, to allow for time
    dependant rates that may be non-zero at later times
    This time step is drawn from an exp dist based on ((t_stop-t_start)/100)

    Parameters
    ----------
    propensities : callable of form propensities(state)
        State is array of length (N+1) of time and count per compartment
        (for N compartments)
        Will return an NxN array as a transition matrix for propensities
    t_span : 2-list of floats
        Internal of integration (t_start, t_end). The solver starts at t_start
        and will finish once the first random time_step exceeds t_end
        (Note that the final value may be greater than t_end)
    initial_cond : array_like, shape (N,)
        Initial state, gives counts in each of N compartments
    max_t_step : float (default value 0.01)
        This is the maximum allowed timestep, as a fraction of the total t_span
        Default value is 0.01, so (t_span[1] - t_span[0])/100
        Note that the exact time_steps are sampled from an exponential
        distribution, and so may be smaller than this

    Yields
    -------
    Numpy array of form [Time, Compartment_1, ...], ie [time, S, E, I, R]
        Note that time steps are random (not uniform), and final timestep lie
        after the end of the time_span given

    """
    if len(t_span) != 2:
        raise ValueError("`t_span must be 2-dimensional - form [start, end]")
    try:
        float(t_span[1]) - float(t_span[0])
    except ValueError:
        raise TypeError("Cannot convert t_span values to float")

    if t_span[0] >= t_span[1]:
        raise ValueError("End time must be after start time")
    if t_span[0] < 0:
        raise ValueError(f"Start time (t = {t_span[0]}) cannot be negative")

    if np.any(np.array(initial_cond) < 0):
        raise ValueError("Cannot have negative elements in initial_cond")

    state = np.zeros(len(initial_cond) + 1)
    state[0] = t_span[0]
    state[1:] = initial_cond

    while state[0] < t_span[1]:
        propensity_values = propensities(state)
        total_rate = np.sum(propensity_values)
        if total_rate == 0:
            total_rate = 1 / ((t_span[1] - t_span[0]) * max_t_step)
        time_step = np.log(1 / np.random.rand()) / total_rate
        state[0] += time_step

        normal_prop = propensity_values / total_rate
        running_tot = 0
        random_proc = np.random.rand()
        for index, value in np.ndenumerate(normal_prop):
            running_tot += value
            if value != 0 and running_tot > random_proc:
                loss, gain = index
                if state[loss + 1] > 0:  # Can't remove counts from empty state
                    state[loss + 1] -= 1  # +1 to skip past time index
                    state[gain + 1] += 1
                break

        yield state
