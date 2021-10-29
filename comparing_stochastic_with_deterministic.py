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
iteration_number = 100
param_variation_number = 50
BETA = np.linspace(0, .2, param_variation_number)

max_infected_stoch = np.zeros((param_variation_number, iteration_number))
max_infected_stoch_max = np.zeros(param_variation_number)
max_infected_stoch_min = np.zeros(param_variation_number)
max_infected_stoch_mean = np.zeros((param_variation_number, 1))
max_infected_stoch_25th_quartile = np.zeros((param_variation_number, 1))
max_infected_stoch_75th_quartile = np.zeros((param_variation_number, 1))
max_infected_determ = np.zeros((param_variation_number, 1))
timeEnd = 1
n_times = 10 * timeEnd + 1
times = np.linspace(0, timeEnd, num=n_times)
i = 0

for i, beta in enumerate(BETA):
    # Set up the deterministic model
    parameter_values = np.array([1000, 0, 20, 0, beta, .1, .1])
    model_determ._parameters.configure_parameters(parameter_values)
    model_determ.set_outputs(seir)
    output = model_determ.simulate(np.array(parameter_values), times)
    infection = output[:, 2]
    max_infected_determ[i] = np.max(infection)

    model_stoch._parameters.configure_parameters(parameter_values)
    model_stoch.set_outputs(seir)
    for j in range(iteration_number):
        output = model_stoch.simulate(np.array(parameter_values), times)
        # problem = p.MultiOutputProblem(model_stoch, times, output)
        infection = output[:, 2]
        max_infected_stoch[i, j] = np.nanmax(infection)
    max_infected_stoch_mean[i] = np.nanmean(max_infected_stoch[i, :])
    max_infected_stoch_max[i] = np.nanmax(max_infected_stoch[i, :])
    max_infected_stoch_min[i] = np.nanmin(max_infected_stoch[i, :])
    max_infected_stoch_25th_quartile[i] = \
        np.percentile(max_infected_stoch[i, :], 25)
    max_infected_stoch_75th_quartile[i] = \
        np.percentile(max_infected_stoch[i, :], 75)


figure = se.plots.ConfigurablePlotter()
figure.begin()
figure.add_data_to_plot(BETA, max_infected_stoch_25th_quartile, xlabel='beta',
                        ylabels=['stochastic 25th quartile'], colours=['b'])
figure.add_data_to_plot(BETA, max_infected_stoch_75th_quartile, xlabel='beta',
                        ylabels=['stochastic 75th quartile'], colours=['b'])
figure.add_data_to_plot(BETA, max_infected_stoch_mean, xlabel='beta',
                        ylabels=['stochastic mean'], colours=['b'])
figure.add_fill(BETA, max_infected_stoch_min, max_infected_stoch_max,
                xlabel='beta', ylabel='stochastic max/min')
figure.add_data_to_plot(BETA, max_infected_determ, xlabel='beta',
                        ylabels=['deterministic'], colours=['r'])
figure.show()
