import seirmo as se
import numpy as np
import pints as p
import pints.plot as pin
import matplotlib.pyplot as plt

model = se.StochasticSEIRModel(['S0', 'E0', 'I0', 'R0', 'beta', 'kappa', 'gamma'])
seir = ['S', 'E', 'I', 'R']
parameter_values = np.array([98, 0, 2, 0, 1, 2, 1])
timeEnd = 10
n_times = 10*timeEnd + 1
times = np.linspace(0, timeEnd, num=n_times)
model._parameters.configure_parameters(parameter_values)
model.set_outputs(seir)

output = model.simulate(np.array(parameter_values), times)
#last = output[-1,1:]
#print(last.shape)
#compare=np.zeros(4)
#print(compare.shape)
problem = p.MultiOutputProblem(model, times, output[:, 1:])

figure = se.plots.StochasticPlotter(output)
figure.plot(seir)
