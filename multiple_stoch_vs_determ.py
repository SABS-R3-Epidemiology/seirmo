#
# This file is part of seirmo (https://github.com/SABS-R3-Epidemiology/seirmo/)
# which is released under the BSD 3-clause license. See accompanying LICENSE.md
# for copyright notice and full license details.
#

import seirmo as se
import numpy as np
import pints as p

model_stoch = se.StochasticSEIRModel(['S0', 'E0', 'I0', 'R0', 'beta', 'kappa',
                                      'gamma'])
model_determ = se.DeterministicSEIRModel()
seir = ['S', 'E', 'I', 'R']
iteration_number = 101
iterations = np.linspace(0, 100, iteration_number)
parameter_values = np.array([1000, 0, 20, 0, .1, .1, .1])
infected_stoch_mean = np.zeros((iteration_number, 1))
infected_stoch_2_5th_quartile = np.zeros((iteration_number, 1))
infected_stoch_97_5th_quartile = np.zeros((iteration_number, 1))
timeEnd = 20
n_times = 10 * timeEnd + 1
times = np.linspace(0, timeEnd, num=n_times)


stoch_infections = np.zeros((n_times, iteration_number))
infection = np.ndarray((n_times,1))


i =0
for iter in iterations:
    
    model_stoch._parameters.configure_parameters(parameter_values)
    model_stoch.set_outputs(seir)
    
    output = model_stoch.simulate(np.array(parameter_values), times)
    stoch_infections[:, i] = np.nan_to_num(output[:, 2])
    i+=1

 # set up the deterministic model


infected_stoch_mean = np.nanmean(stoch_infections, axis=1)
infected_stoch_2_5th_quartile = np.nanpercentile(stoch_infections, 2.5, axis=1)
infected_stoch_97_5th_quartile = np.nanpercentile(stoch_infections, 97.5, axis=1)
model_determ._parameters.configure_parameters(parameter_values)
model_determ.set_outputs(seir)
output = model_determ.simulate(np.array(parameter_values), times)
infection[:,0] = output[:, 2]

figure = se.plots.ConfigurablePlotter()
figure.begin()
figure.add_data_to_plot(times, infection, xlabel='time', ylabels=['deterministic'], colours=['r'])
print(infected_stoch_mean.shape)
figure.add_data_to_plot(times, infected_stoch_mean, xlabel='time', ylabels=['stochastic'], colours=['b'])
figure.add_data_to_plot(times, infected_stoch_2_5th_quartile, xlabel='time', ylabels=['2.5th percentile'], colours=['b'])
figure.add_data_to_plot(times, infected_stoch_97_5th_quartile, xlabel='time', ylabels=['97.5th percentile'], colours=['b'])
figure.add_fill(times, infected_stoch_2_5th_quartile, infected_stoch_97_5th_quartile,
                xlabel='times', ylabel='stochastic interval')

figure.show()
