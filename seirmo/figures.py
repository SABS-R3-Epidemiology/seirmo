#
# This file is part of seirmo (https://github.com/SABS-R3-Epidemiology/seirmo/)
# which is released under the BSD 3-clause license. See accompanying LICENSE.md
# for copyright notice and full license details.
#

import plotly.graph_objects as go


class IncidenceNumberPlot(object):
    """

    Creates incidence number plots for the app

    """
    def __init__(self):
        super(IncidenceNumberPlot, self).__init__()

        # Instantiate an empty plotly figure
        self._fig = go.Figure()

    def add_data(self, pandas_DataFrame, time_key='Time',
                 inc_key='Incidence Number'):

        # Plot a bar chart for the data
        self._fig.add_trace(
            go.Bar(
                x=pandas_DataFrame[time_key],
                y=pandas_DataFrame[inc_key],
                name='cases'
            )
        )

        # Add axis labels
        self._fig.update_layout(
            xaxis_title=time_key,
            yaxis_title=inc_key
        )

    def add_simulation(self, pandas_DataFrame, time_key='Time',
                       inc_key='Incidence Number'):

        # Plot a bar chart for the simulation
        self._fig.add_trace(
            go.Bar(
                x=pandas_DataFrame[time_key],
                y=pandas_DataFrame[inc_key],
                name='simulation'
            )
        )

        # Add axis labels
        self._fig.update_layout(
            xaxis_title=time_key,
            yaxis_title=inc_key
        )

    def show(self):

        # Display the figure
        self._fig.show()
