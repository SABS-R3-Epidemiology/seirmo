#
# This file is part of seirmo (https://github.com/SABS-R3-Epidemiology/seirmo/)
# which is released under the BSD 3-clause license. See accompanying LICENSE.md
# for copyright notice and full license details.
#

import seirmo as se
import numpy as np

model_stoch = se.StochasticSEIRModel(['S0', 'E0', 'I0', 'R0', 'beta', 'kappa',
                                      'gamma'])
model_determ = se.DeterministicSEIRModel()
seir = ['S', 'E', 'I', 'R']
iteration_number = 101
iterations = np.linspace(0, 100, iteration_number)
parameter_values = np.array([1000, 0, 20, 0, .1, .1, .1])
timeEnd = 10
n_times = 10 * timeEnd + 1
times = np.linspace(0, timeEnd, num=n_times)


stoch_infections = np.zeros((n_times, iteration_number))
infection = np.ndarray((n_times, 1))

figure = se.plots.ConfigurablePlotter()
figure.begin()
for index, iter in enumerate(iterations):

    model_stoch._parameters.configure_parameters(parameter_values)
    model_stoch.set_outputs(seir)

    output = model_stoch.simulate(np.array(parameter_values), times)
    stoch_infections[:, index] = output[:, 2]
    figure.add_data_to_plot(times, stoch_infections[:, [index]], xlabel='time',
                            ylabels='number of infected')


# Set up the deterministic model
model_determ._parameters.configure_parameters(parameter_values)
model_determ.set_outputs(seir)
output = model_determ.simulate(np.array(parameter_values), times)
infection[:, 0] = output[:, 2]
print(infection.shape)
figure.add_data_to_plot(times, infection, xlabel='time',
                        ylabels='number of infected')

figure.show()
