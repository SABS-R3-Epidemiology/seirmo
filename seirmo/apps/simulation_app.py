#
# This file is part of seirmo (https://github.com/SABS-R3-Epidemiology/seirmo/)
# which is released under the BSD 3-clause license. See accompanying LICENSE.md
# for copyright notice and full license details.
#

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import pandas as pd

import seirmo as se
import seirmo.apps as sapps


class SimulationApp(object):
    """SimulationApp Class:

    Creates the SEIR model simulation app.

    """

    def __init__(self):
        super(SimulationApp, self).__init__()

        self._fig_plot = se.IncidenceNumberPlot()
        self._slider_component = sapps._SliderComponent()

        self.simulation_start = 0
        self.simulation_end = 50

    def _set_layout(self):
        """
        Create the layout of the app.
        """

        self.app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

        self.app.layout = dbc.Container(
            dbc.Row([
                    dbc.Col([dcc.Graph(
                            figure=self._fig_plot._fig, id='fig')],
                            style={"height": "90vh"}, width=6, md=8
                            ),
                    dbc.Col([
                        self._slider_component()])
                    ])
        )

    def add_data(self, data, time_key='Time', inc_key='Incidence Number'):
        """
        Plot figure for given incidence number data.

        Parameters
        ----------
        data
            A pandas.DataFrame with 2 columns, one being time points,
            the other being incidence number.
        time_key
            Key label of the DataFrame which specifies the time points.
            Defaults to 'Time'.
        inc_key
            Key label of the DataFrame which specifies the
            incidence number.
            Defaults to 'Incidence Number'.
        """

        if not isinstance(data, pd.DataFrame):
            raise TypeError(
                'Data has to be an instance of pandas.DataFrame.')

        if time_key not in data.columns:
            raise ValueError(
                'The input time key does not match that in the data.')

        if inc_key not in data.columns:
            raise ValueError(
                'The input incidence key does not match that in the data.')

        self._fig_plot.add_data(
            data, time_key, inc_key)

    def add_model(self, model, parameters_name, total_population):
        """
        Plot figure of simulation for given model.

        Parameters
        ----------
        model
            A subclass of seirmo.ForwardModel class, which specifies
            the model of simulation.
        parameters_name
            Name of parameters of model in list of strings.
        """

        parameters_name = list(parameters_name)

        init_parameters = []
        for model_parameter in parameters_name[:4]:
            model_parameter = str(model_parameter)
            self._slider_component.add_slider(
                slider_id=model_parameter,
                min_value=0 * total_population,
                max_value=1 * total_population,
                initial_value=0.5 * total_population)
            init_parameters.append(
                self._slider_component._sliders[model_parameter].children[1].value) # noqa

        for model_parameter in parameters_name[4:]:
            model_parameter = str(model_parameter)
            self._slider_component.add_slider(
                slider_id=model_parameter,
                min_value=0,
                max_value=1,
                initial_value=0.5)
            init_parameters.append(
                self._slider_component._sliders[model_parameter].children[1].value) # noqa

        self._slider_component.group_sliders(
            parameters_name, 'Sliders of parameters')

        self.simulate = se.SimulationController(
            model, self.simulation_start, self.simulation_end)

        data = self.simulate.run(init_parameters, return_incidence=True)
        data = pd.DataFrame({
            'Time': list(self.simulate._simulation_times),
            'Incidence Number': data[:, -1]
        })
        self._fig_plot.add_simulation(data)

    def slider_ids(self):
        """
        Return the ids of sliders added to the app.
        """
        return self._slider_component.get_slider_ids()

    def update_simulation(self, parameters):
        """
        Update the figure with simulated data of new parameters.

        Parameters
        ----------
        parameters
            List of parameter values for simulation.
        """
        data = self.simulate.run(parameters, return_incidence=True)
        self._fig_plot._fig['data'][1]['y'] = data[:, 1]

        return self._fig_plot._fig
