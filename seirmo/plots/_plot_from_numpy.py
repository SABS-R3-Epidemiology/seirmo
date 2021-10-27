
import numpy as np
import matplotlib.pyplot as plt


class StochasticPlotter():
    def __init__(self, data_array: np.array):
        self._data = data_array

    def plot(self, labels: list, filename: str = 'SEIR_stochastic_simulation.png'):
        new_data = self.remove_zero_row()
        time = new_data[:, 0]
        data = new_data[:, 1:]
        fig, axes = plt.subplots()
        colours = plt.cm.viridis(np.linspace(0, 1, len(labels)))
        for i in range(4):
            axes.plot(time, data[:, i], color=colours[i], 
                      label=labels[i])
        axes.legend()
        plt.xlabel('time')
        fig.tight_layout()
        fig.savefig(filename)
        plt.show()

    def remove_zero_row(self):
        for i in range(len(self._data.shape[0])):
            if self._data[i, 1:] != np.zeros(4):
                i += 1
        self._reduced_data = self._data[:i+1, :]
        return self._reduced_data

