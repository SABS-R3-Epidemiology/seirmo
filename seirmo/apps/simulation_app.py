#
# This file is part of seirmo (https://github.com/SABS-R3-Epidemiology/seirmo/)
# which is released under the BSD 3-clause license. See accompanying LICENSE.md
# for copyright notice and full license details.
#

import seirmo as se

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html


class SimulationApp(object):
    """SimulationApp Class:

    Creates the SEIR model simulation app.

    """

    def __init__(self):
        super(SimulationApp, self).__init__()

        IncidenceNumberPlot = se.IncidenceNumberPlot()
        SliderComponent = se._SliderComponent()

        app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

        app.layout = dbc.Container(
        dbc.Row(
            [
                dbc.Col(html.Div("One of two columns")),
                dbc.Col(html.Div("One of two columns")),
            ]
        ),
        )

    def add_data(self):
        """
        """
        
    def add_model(self, model, parameters_name):

        for model_parameter in parameters_name:
            SliderComponent.add_slider(slider_id = model_parameter,
                                        min_value = 0,
                                        max_value = 1)
        
        simulate = se.SimulationController(model,0,40)
        initial_parameters_value = [0]*len(parameters_name)
        data = simulate.run(initial_parameters_value, return_incidence=True)
        IncidenceNumberPlot.add_data(data)

if __name__ == "__main__":
    app.run_server()