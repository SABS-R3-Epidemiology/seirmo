import seirmo as se
import numpy as np
import pints as p
# import pints.plot as pin
# import matplotlib.pyplot as plt

model = se.StochasticSEIRModel(['S0', 'E0', 'I0', 'R0',
                                'beta', 'kappa', 'gamma'])
seir = ['S', 'E', 'I', 'R']
parameter_values = np.array([90, 10, 0, 0, 1, 2, 1])
timeEnd = 10
n_times = 10 * timeEnd + 1
times = np.linspace(0, timeEnd, num=n_times)
model._parameters.configure_parameters(parameter_values)
model.set_outputs(seir)

output = model.simulate(np.array(parameter_values), times)
problem = p.MultiOutputProblem(model, times, output)

figure = se.plots.StochasticPlotter(output)
figure.plot(seir)
