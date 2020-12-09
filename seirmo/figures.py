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

        """
        Add a bar plot trace for the given incidence number data
        in the figure

        Parameters
        ----------
        data: pandas.DataFrame
        time_key: docstring
        inc_key: docstring
        """
    def add_data(self, data, time_key='Time',
                 inc_key='Incidence Number'):

        # Plot a bar chart for the data
        self._fig.add_trace(
            go.Bar(
                x=data[time_key],
                y=data[inc_key],
                name='cases'
            )
        )

        # Add axis labels; Raise error when the x and y axis labels
        # do not match the old ones if they already exist;
        # otherwise update the labels
        old_x_label = self._fig['layout']['xaxis']['title']['text']
        old_y_label = self._fig['layout']['yaxis']['title']['text']
        print(old_x_label)
        print(old_y_label)

        if (old_x_label or old_y_label):
            if old_x_label != time_key or old_y_label != inc_key:
                raise ValueError(
                    'The x and y labels do not match the old ones.')
        else:
            self._fig.update_layout(
                xaxis_title=time_key,
                yaxis_title=inc_key
            )

        """
        Add a bar plot trace for the simulated incidence numbers
        in the figure

        Parameters
        ----------
        data: pandas.DataFrame
        time_key: docstring
        inc_key: docstring
        """
    def add_simulation(self, data, time_key='Time',
                       inc_key='Incidence Number'):

        # Plot a bar chart for the simulation
        self._fig.add_trace(
            go.Bar(
                x=data[time_key],
                y=data[inc_key],
                name='simulation'
            )
        )

        # Add axis labels; Raise error when the x and y axis labels
        # do not match the old ones if they already exist;
        # otherwise update the labels
        old_x_label = self._fig['layout']['xaxis']['anchor']
        old_y_label = self._fig['layout']['yaxis']['anchor']
        if (old_x_label or old_y_label):
            if old_x_label != time_key or old_y_label != inc_key:
                raise ValueError(
                    'The x and y labels do not match the old ones.')
        else:
            self._fig.update_layout(
                xaxis_title=time_key,
                yaxis_title=inc_key
            )

    def show(self):

        # Display the figure
        self._fig.show()
