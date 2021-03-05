#
# This file is part of seirmo (https://github.com/SABS-R3-Epidemiology/seirmo/)
# which is released under the BSD 3-clause license. See accompanying LICENSE.md
# for copyright notice and full license details.
#

"""This is an app which shows forward simulation of the SEIR model
with fixed example data. To run the app, use ``python dash_app.py``.
"""

import dash
from dash.dependencies import Input, Output, State
import dash_html_components as html

import seirmo as se
from seirmo import apps

# Instantiate app
app = apps._OptimisationApp()

# Add french flu data
flu_data = se.DatasetLibrary().french_flu()
flu_data = flu_data.rename(
    columns={'time_index': 'Time', 'inc': 'Incidence Number'})
flu_data = flu_data.loc[60:90, :]
flu_data['Time'] = flu_data['Time'] - flu_data['Time'].min()
flu_data['Incidence Number'] = flu_data['Incidence Number'] / 1e5

# Instantiate model and add simulation to figure
model = se.SEIRModel

parameters_name = [
    'Initial S', 'Initial E', 'Initial I', 'Initial R',
    'Infection Rate', 'Incubation Rate', 'Recovery Rate']

app.add_problem(flu_data, model)

# Get subplots for the figure
app.get_subplots()
app._subplot_fig._fig.update_yaxes(
    title_text='Incidence Number <br> (100K)', row=1, col=1)
app._subplot_fig._fig.update_yaxes(
    title_text='Number of individuals <br> (100K)', row=2, col=1)

# Set layout of app
app._set_layout()

# Add title
title = 'SEIR model - optimisation'

server = app.app.server


@app.app.callback(
    [Output('fig', 'figure'),
        Output('inferred-parameters-table', 'data'),
        Output("run-optimisation", "children")],
    [Input('run-button', 'n_clicks'),
        Input('reset-button', 'n_clicks')],
    State('fig', 'figure'))
def update_simulation(n_clicks, *args):
    """
    Simulates the model for the current slider values and updates the
    subplots in the figure when the Run button is clicked.
    Reset the app when the Reset button is clicked.
    """
    ctx = dash.callback_context
    if ctx.triggered:
        input_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if input_id == "reset-button":
            fig, table, display = app.reset()
        else:
            fig, table, display = app.update_simulation(n_clicks)
        return fig, table, display
    else:
        fig, table, display = app.update_simulation(n_clicks)
        return fig, table, display


@app.app.callback(
    Output("fixed-parameters-output", "children"),
    [Input(param, 'value') for param in parameters_name])
def update_model(*args):
    """
    Set up reduced model
    """
    fixed_parameters = list(args)
    app.update_model(fixed_parameters)

    output = []
    for i in range(len(parameters_name)):
        output.append(parameters_name[i] + ' = {}'.format(fixed_parameters[i]))
        output.append(html.Br())

    return html.P(output)


if __name__ == "__main__":
    app.app.run_server(debug=True)
