import seirmo as se
import numpy as np
import pints as p
import pints.plot as pin
import matplotlib.pyplot as plt

model = se.StochasticSEIRModel(['S0', 'E0', 'I0', 'R0', 'beta', 'kappa', 'gamma'])
seir = ['S', 'E', 'I', 'R']
parameter_values = np.array([90, 10, 0, 0, 1, 2, 1])
timeEnd = 10
n_times = 10*timeEnd + 1
times = np.linspace(0, timeEnd, num=n_times)
model._parameters.configure_parameters(parameter_values)
model.set_outputs(seir)

output = model.simulate(np.array(parameter_values), times)
print(output)
problem = p.MultiOutputProblem(model, times, output[:, 1:])

# fig = plt.series(output[:, 1:], problem)
time = output[:timeEnd*9, 0]

data = output[: timeEnd*9, 1:]
fig, axes1 = plt.subplots()
colours = plt.cm.viridis(np.linspace(0, 1, len(seir)))
for i in range(4):
    axes1.plot(time, data[:, i], color=colours[i], 
               label=seir[i])
axes1.legend()
plt.xlabel('time [h]')
        
fig.tight_layout()
#fig.savefig(fig_file)  # may need to change which directory it saves in
plt.show()
