import seirmo as se
import numpy as np

model = se.StochasticSEIRModel(['S0', 'E0', 'I0', 'R0', 'beta', 'kappa',
                               'gamma'])
seir = ['S', 'E', 'I', 'R']
parameter_values = np.array([100, 0, 2, 0, 0.1, 1, 1])
timeEnd = 10
n_times = 1000 * timeEnd + 1
times = np.linspace(0, timeEnd, num=n_times)
model._parameters.configure_parameters(parameter_values)
model.set_outputs(seir)

output = model.simulate(np.array(parameter_values), times)

figure = se.plots.ConfigurablePlotter()
figure.begin()
figure.add_data_to_plot(times, output, ylabels=seir)
figure.show()

figure = se.plots.ConfigurablePlotter()
figure.begin(2, 2)
figure.add_data_to_plot(times, output[:, 0:], ylabels='S', position=[0, 0])
figure.add_data_to_plot(times, output[:, 1:], ylabels='E', position=[0, 1])
figure.add_data_to_plot(times, output[:, 2], ylabels='I', position=[1, 0])
figure.add_data_to_plot(times, output[:, :3], ylabels='R', position=[1, 1])
figure.show()
