import seirmo as se
import numpy as np

model = se.StochasticSEIRModel(['S0', 'E0', 'I0', 'R0', 'beta', 'kappa',
                               'gamma'])
seir = ['S', 'E', 'I', 'R']
parameter_values = np.array([100, 0, 2, 0, 0.1, 1, 1])
timeEnd = 10
n_times = 10000 * timeEnd + 1
times = np.linspace(0, timeEnd, num=n_times)
model._parameters.configure_parameters(parameter_values)
model.set_outputs(seir)

output = model.simulate(np.array(parameter_values), times)

figure = se.plots.ConfigurablePlotter()
figure.begin()
figure.add_data_to_plot(times, output, ylabels=seir)
#figure.add_data_to_plot(output[:, 0], output[:, 3:],
                      #  ylabels=['i', 'r'], new_axis=True)
figure.show()
