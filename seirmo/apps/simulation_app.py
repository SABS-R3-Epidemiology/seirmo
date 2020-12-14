#
# This file is part of seirmo (https://github.com/SABS-R3-Epidemiology/seirmo/)
# which is released under the BSD 3-clause license. See accompanying LICENSE.md
# for copyright notice and full license details.
#

import pandas as pd
import seirmo as se

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc


class SimulationApp(object):
    """SimulationApp Class:

    Creates the SEIR model simulation app.

    """

    def __init__(self):
        super(SimulationApp, self).__init__()

        self.IncidenceNumberPlot = se.IncidenceNumberPlot()
        self.SliderComponent = se._SliderComponent()

        self.app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

        self.app.layout = dbc.Container(
            dbc.Row(
                [
                    dbc.Col(
                        dcc.Graph(
                            figure=self.IncidenceNumberPlot._fig, id='fig')),
                    dbc.Col(
                        [dbc.Row(
                            self.SliderComponent.group_sliders(
                                self.slider_ids()[:4], 'init_value')),
                         dbc.Row(
                            self.SliderComponent.group_sliders(
                                self.slider_ids()[4:], 'constant'))]
                    )
                ]
            )
        )

        self.simulation_start = 0
        self.simulation_end = 50

    def add_data(self, data):
        """
        """
        self.IncidenceNumberPlot.add_data(
            data, time_key='Time', inc_key='Incidence Number')

    def add_model(self, model, parameters_name):

        for model_parameter in parameters_name:
            self.SliderComponent.add_slider(slider_id=model_parameter,
                                            min_value=0,
                                            max_value=1)

        self.simulate = se.SimulationController(
            model, self.simulation_start, self.simulation_end)
        init_parameters = [0] * len(parameters_name)
        data = self.simulate.run(init_parameters, return_incidence=True)
        data = pd.DataFrame(data, columns=['Time', 'Incidence Number'])
        self.IncidenceNumberPlot.add_simulation(data)

    def slider_ids(self):
        return self.SliderComponent.get_slider_ids()

    def update_simulation(self, parameters):
        data = self.simulate.run(parameters, return_incidence=True)
        self.IncidenceNumberPlot._fig['data'][0]['y'] = data[:, 1]
