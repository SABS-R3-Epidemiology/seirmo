#
# This file is part of seirmo (https://github.com/SABS-R3-Epidemiology/seirmo/)
# which is released under the BSD 3-clause license. See accompanying LICENSE.md
# for copyright notice and full license details.
#

"""This is an app which shows forward simulation of the SEIR model
with fixed example data. To run the app, use ``python dash_app.py``.
"""

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import numpy as np
import os
import pandas as pd
import random

import seirmo as se
from seirmo import apps

# Instantiate app
app = apps._SimulationApp()

# Create random data and add to figure
data = pd.DataFrame({
    'Time': range(50),
    'Incidence Number': [random.randint(0, 3000) for i in range(50)]})
app.add_data(data)

# Instantiate model and add simulation to figure
model = se.SEIRModel
parameter_name = ['Total Population', 'Initial S', 'Initial E', 'Initial I',
                  'Initial R', 'Infection Rate', 'Incubation Rate',
                  'Recovery Rate']
total_population = 10000
app.add_model(model, parameter_name, total_population)

# Set layout of app
app._set_layout()

# Identify  and keep figure and sliders of app
fig_slider = app.app.layout.children[0]

# Add title
title = 'SEIR model'

# Model motivation
motivation = """
Scientists and researchers are trying to understand the COVID-19 in hopes to predict and defeat the 
disease. In order to understand the spread and infecting rate of the disease, many models are used 
to characterise the disease, such as the SEIR model and the branching processes model.  
SEIR model is a deterministic model and has been used to model infectious disease.  
"""

# Model description
description = """
The SEIR model is a model of Ordinary Differential Equations (ODEs). 
It assigns a population into 4 compartments, which are Susceptible(S), Exposed(E), Infectious(I) 
and Recovered(R). In this model, individuals will transit from being Susceptible to Exposed, from 
Exposed to Infectious and from Infectious to Recovered. To control the rate at which the individuals
transit from one state to the other, some parameters are imposed in the model.  
  
The model is characterised by few constants, which includes *reproduction number*, *incubation period* 
and *infection period*. The *reproduction number* measures the number of infected cases reproduced 
from primary infections, the *incubation period* defines the average period of time for exposed 
individuals to become infectious, and the *infection period* is the average period of time for 
infected patients to recover from the disease.  
  
The system of ODEs is solved to retrieve number of inviduals in each S, E, I and R compartments. The
incidence number is then inferred from the solution. To solve the system of ODEs, the initial value of
each compartment is required. Different initial values will give different solution. It would be clear 
that changing the initial values of S, E, I and R will change the simulated incidence numbers, after
you play around with the sliders.   
"""

reference = """
[1] He, S., Peng, Y. & Sun, K. SEIR modeling of the COVID-19 and its dynamics. *Nonlinear Dyn*
 **101**, 1667-1680 (2020).
"""

app.app.layout = dbc.Container(children=[
    html.H1(title),
    dcc.Markdown(motivation),
    dcc.Markdown(description),
    html.Br(),
    fig_slider,
    dcc.Markdown(reference)
])
print(app.app.layout)

# Get sliders for callback
sliders = app.slider_ids()

@app.app.callback(
    Output('fig', 'figure'),
    [Input(s, 'value') for s in sliders])
def update_simulation(*args):
    """
    Simulates the model for the current slider values and updates the
    plot in the figure.
    """
    parameters = list(args)
    fig = app.update_simulation(parameters)
    # print(parameters)

    return fig


if __name__ == "__main__":
    app.app.run_server(
        host=os.getenv('IP', '0.0.0.0'),
        port=int(os.getenv('PORT', 4444)), debug=True)
