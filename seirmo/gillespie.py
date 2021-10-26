#
# This file is part of seirmo (https://github.com/SABS-R3-Epidemiology/seirmo/)
# which is released under the BSD 3-clause license. See accompanying LICENSE.md
# for copyright notice and full license details.
#

import numpy as np
import typing


def solve_gillespie(propensities: typing.Callable[[np.ndarray], np.ndarray],
                    initial_cond: np.ndarray, t_span: typing.List[float]):
    """ Solve an initial_cond value problem using gillespie algorithm

    This function numerically integrates a system of ordinary differential
    equations given initial_cond conditions. We use the Gillespie algorithm
    with tau-leaping, so that the time step is not uniform but sampled randomly

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

    Yields
    -------
    Numpy array of form [Time, Compartment_1, ...], ie [time, S, E, I, R]
        Note that time steps are random (not uniform), and final timestep lie
        after the end of the time_span given

    """
    if len(t_span) != 2:
        raise ValueError("`t_span must be 2-dimensional - form [start, end]")
    if t_span[0] >= t_span[1]:
        raise ValueError("End time must be after start time")
    if t_span[0] < 0:
        raise ValueError(f"Start time (t = {t_span[0]}) cannot be negative")
    try:
        float(t_span[1]) - float(t_span[0])
    except ValueError:
        raise TypeError("Cannot convert t_span values to float")

    if np.any(initial_cond < 0):
        raise ValueError("Cannot have negative elements in initial_cond")

    state = np.zeros(len(initial_cond) + 1)
    state[0] = t_span[0]
    state[1:] = initial_cond

    while state[0] < t_span[1]:
        propensities = propensities(state)
        total_rate = np.sum(propensities)
        time_step = np.log(1 / np.random.rand()) / total_rate
        state[0] += time_step

        normal_prop = propensities / total_rate
        running_tot = 0
        random_proc = np.random.rand()
        for index, value in np.ndenumerate(normal_prop):
            running_tot += value
            if value != 0 and running_tot > random_proc:
                loss, gain = index
                state[loss + 1] -= 1  # +1 to skip past time index
                state[gain + 1] += 1
                break

        yield state
