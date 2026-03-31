#
# This file is part of seirmo (https://github.com/SABS-R3-Epidemiology/seirmo/)
# which is released under the BSD 3-clause license. See accompanying LICENSE.md
# for copyright notice and full license details.
#

"""This is an app which shows forward simulation of the SEIR model
with fixed example data. To run the app, use ``python dash_app.py``.
"""

import base64
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import numpy as np
import os
import pandas as pd
import random

import seirmo as se
from seirmo import apps

# Instantiate app
app = apps._SimulationApp()

# Add french flu data
flu_data = se.DatasetLibrary().french_flu()
flu_data = flu_data.loc[:30,:]
flu_data['inc'] = flu_data['inc']
app.add_data(flu_data, time_key='time_index', inc_key='inc')

# Instantiate model and add simulation to figure
model = se.SEIRModel
parameter_name = [
    'Initial S', 'Initial E', 'Initial I', 'Initial R',
    'Infection Rate', 'Incubation Rate', 'Recovery Rate']
total_population = 650000
app.add_model(model, parameter_name)

# Get subplots for the figure
app.get_subplots()

# Set layout of app
app._set_layout()

# Identify  and keep figure and sliders of app
fig_slider = app.app.layout.children[0]

for slider in parameter_name[:4]:
    app._slider_component._sliders[slider].children[1].max = total_population
    app._slider_component._sliders[slider].children[1].value = total_population / 2
    app._slider_component._sliders[slider].children[1].step = 1
    app._slider_component._sliders[slider].children[1].marks = {
        int(i): (' ') for i in np.linspace(
            start=0,
            stop=total_population,
            num=11
        )
    }

# Add title
title = 'SEIR model'

# Model motivation
motivation = """
Scientists and researchers are trying to understand the COVID-19 outbreak in hopes to
 predict and defeat the disease. In order to understand the spread and
 the infecting rate of the disease, many models are used to characterise the
 disease, such as the SEIR model and the branching processes model.

The SEIR model is a deterministic model, which means that the simulations will always
be the same as long as the parameters are the same.  """

# Model description
description1 = """
The SEIR model assigns individuals in a population to four distinct disease stages:
Susceptible(S), Exposed(E), Infectious(I) and Recovered(R). Exposed individuals are infected but
 not infectious. Susceptible individuals can become infected, then infectious and ultimately recover.
 Diagrammatically this may be illustrated by the figure below.  """

description2 = """

More formally, the SEIR model is expressed in terms of a system of ordinary differential equations.
The transition rates between the states are controlled by rate parameters. The
*infection rate* indicates the speed at which an individual from the S gets exposed and enters the
group E. The *incubation rate* explains how fast an individual who got exposed becomes infected. For
example, if the incubation rate of the disease is higher, then individuals get infected quickly once
it is exposed. Finally, the rate where infected individuals get recovered is described by the *recovery
rate*.  """

plot_description = """
The bar graph shows the daily incidence number of an infectious disease. The blue bars show actual
cases of infectious disease while the red ones show cases simulated by the SEIR model, given the
parameters of the sliders.

In this model, an individual in a population will start with being susceptible, then exposed to
the disease, get infected and finally recovers from the disease. Therefore, in the second plot,
number of individuals in group S, E and I will eventually approach zero, while group R will
eventually include everyone in the population. However, for an infectious disease to spread,
it will require an initial amount of cases, that is the initial amount of exposed and infected
individuals, to be nonzero.

You are welcome to explore the effect of initial sizes of the S, E, I and R groups, as well as
the different transition periods with the parameter sliders below.
"""

reference = """
[1] He, S., Peng, Y. & Sun, K. SEIR modeling of the COVID-19 and its dynamics. *Nonlinear Dyn*
 **101**, 1667-1680 (2020).
"""
fname = os.path.join(os.path.dirname(__file__), 'descriptions', 'SEIR_image.png')

encoded_image = base64.b64encode(open(fname, 'rb').read())

app.app.layout = dbc.Container(children=[
    html.H1(title),
    html.H4('Motivation'),
    dcc.Markdown(motivation),
    html.H4('Description'),
    dcc.Markdown(description1),
    html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()),
        style={'width': '1000px'}),
    dcc.Markdown(description2),
    html.H4('Simulation and real data'),
    dcc.Markdown(plot_description),
    html.Br(),
    fig_slider,
    # dcc.Markdown(reference),
])

# Get sliders for callback
sliders = app.slider_ids()

server = app.app.server

@app.app.callback(
    Output('fig', 'figure'),
    [Input(s, 'value') for s in sliders])
def update_simulation(*args):
    """
    Simulates the model for the current slider values and updates the
    subplots in the figure.
    """
    parameters = list(args)
    fig = app.update_simulation(parameters)

    return fig


if __name__ == "__main__":
    app.app.run_server(
        host=os.getenv('IP', '0.0.0.0'),
        port=int(os.getenv('PORT', 4444)), debug=True)
