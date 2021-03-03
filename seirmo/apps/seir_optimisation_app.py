#
# This file is part of seirmo (https://github.com/SABS-R3-Epidemiology/seirmo/)
# which is released under the BSD 3-clause license. See accompanying LICENSE.md
# for copyright notice and full license details.
#

"""This is an app which shows forward simulation of the SEIR model
with fixed example data. To run the app, use ``python dash_app.py``.
"""

from dash.dependencies import Input, Output, State
import os

import seirmo as se
from seirmo import apps

# Instantiate app
app = apps._OptimisationApp()

# Add french flu data
flu_data = se.DatasetLibrary().french_flu()
flu_data = flu_data.rename(columns={'time_index': 'Time', 'inc': 'Incidence Number'})
flu_data = flu_data.loc[60:90, :]
flu_data['Time'] = flu_data['Time'] - flu_data['Time'].min()
flu_data['Incidence Number'] = flu_data['Incidence Number'] / 1e5
# app.add_data(flu_data, time_key='Time', inc_key='Incidence Number')

# Instantiate model and add simulation to figure
model = se.SEIRModel

parameter_name = [
    'Initial S', 'Initial E', 'Initial I', 'Initial R',
    'Infection Rate', 'Incubation Rate', 'Recovery Rate']
# app.add_model(model, parameter_name)

app.add_problem(flu_data, model)

# Get subplots for the figure
app.get_subplots()

# Set layout of app
app._set_layout()

# Add title
title = 'SEIR model - optimisation'

# fname = os.path.join(os.path.dirname(__file__), 'descriptions', 'SEIR_image.png')

# encoded_image = base64.b64encode(open(fname, 'rb').read())
# content = app.app.layout.children[0]

# app.app.layout = dbc.Container(children=[
#     html.H1(title),
#     html.H4('Motivation'),
#     dcc.Markdown(motivation),
#     html.H4('Description'),
#     dcc.Markdown(description1),
#     html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()),
#         style={'width': '1000px'}),
#     dcc.Markdown(description2),
#     html.H4('Simulation and real data'),
#     dcc.Markdown(plot_description),
#     html.Br(),
#     fig_slider,
#     dcc.Markdown(reference),
# ])

server = app.app.server


@app.app.callback(
    [Output('fig', 'figure'),
        Output('inferred-parameters-table', 'data')],
    Input('run-button', 'n_clicks'),
    State('fig', 'figure'))
def update_simulation(n_clicks, *args):
    """
    Simulates the model for the current slider values and updates the
    subplots in the figure.
    """
    fig, table = app.update_simulation(n_clicks)

    return fig, table


@app.app.callback(
    Output("fixed-parameters-output", "children"),
    Input("Initial R", "value"))
def update_model(R0, *args):
    """
    Set up reduced model
    """
    app.update_model(R0)

    return u'Initial R = {}'.format(R0)


if __name__ == "__main__":
    # app.app.run_server(
    #     host=os.getenv('IP', '0.0.0.0'),
    #     port=int(os.getenv('PORT', 4444)), debug=True)
    app.app.run_server(debug=True)
