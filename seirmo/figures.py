#
# This file is part of seirmo (https://github.com/SABS-R3-Epidemiology/seirmo/)
# which is released under the BSD 3-clause license. See accompanying LICENSE.md
# for copyright notice and full license details.
#

import plotly.graph_objects as go

import warnings


class IncidenceNumberPlot(object):
    """

    A figure class that illustrates the incidence number time
    series as a bar plot over time.

    """
    def __init__(self):
        super(IncidenceNumberPlot, self).__init__()

        # Instantiate an empty plotly figure
        self._fig = go.Figure()

    def add_data(
            self, data, time_key='Time', inc_key='Incidence Number'):
        """

        Add a bar plot trace for the given incidence number data
        in the figure

        Parameters
        ----------
        data
            A pandas.DataFrame with two columns, one being time points,
            the other being incidence number.
        time_key
            Key label of the DataFrame which specifies the time points.
            Defaults to 'Time'.
        inc_key
            Key label of the DataFrame which specifies the
            incididence number. Defaults to 'Incidence Number'.

        """
        # Plot a bar chart for the data
        self._fig.add_trace(
            go.Bar(
                x=data[time_key],
                y=data[inc_key],
                name='cases'
            )
        )

        # Update axis labels
        x_label = time_key
        y_label = inc_key
        self._update_axis_labels(x_label, y_label)

    def add_simulation(self, data, time_key='Time',
                       inc_key='Incidence Number'):
        """

        Add a bar plot trace for the simulated incidence numbers
        in the figure

        Parameters
        ----------
        data
            A pandas.DataFrame with two columns, one being time points,
            the other being incidence number.
        time_key
            Key label of the DataFrame which specifies the time points.
            Defaults to 'Time'.
        inc_key
            Key label of the DataFrame which specifies
            the incididence number. Defaults to 'Incidence Number'.

        """

        # Plot a bar chart for the simulation
        self._fig.add_trace(
            go.Bar(
                x=data[time_key],
                y=data[inc_key],
                name='simulation'
            )
        )

        # Update axis labels
        x_label = time_key
        y_label = inc_key
        self._update_axis_labels(x_label, y_label)

    def _update_axis_labels(self, x_label, y_label):

        old_x_label = self._fig['layout']['xaxis']['title']['text']
        old_y_label = self._fig['layout']['yaxis']['title']['text']

        # Raise warning when the x axis label (time)
        # does not match the old one if it already exist;
        if (old_x_label is not None) and (old_x_label != x_label):
            warnings.warn(
                '''The time key does not match the previous time label.
                   The x label was set to the new time key,
                   but may no longer be appropriate for
                   the previously set data.''')

        # Raise warning when the y axis label (incidence)
        # does not match the old one if it already exist;
        if (old_y_label is not None) and (old_y_label != y_label):
            warnings.warn(
                '''The incidence key does not match the previous incidence label.
                   The y label was set to the new incidence key,
                   but may no longer be appropriate for
                   the previously set data.''')

        # Update axes
        self._fig.update_layout(
            xaxis_title=x_label,
            yaxis_title=y_label
        )

    def show(self):

        # Display the figure
        self._fig.show()


class CompartmentPlot(object):
    """

    A figure class that illustrates the compartment number time
    series as a line plot over time.

    """
    def __init__(self):
        super(CompartmentPlot, self).__init__()

        # Instantiate an empty plotly figure
        self._fig = go.Figure()

    def add_simulation(self, data, time_key='Time', S_key='S',
                       E_key='E', I_key='I', R_key='R'):
        """

        Add line plot traces for the simulated compartment numbers
        in the figure

        Parameters
        ----------
        data
            A pandas.DataFrame with four columns: time points, S, E, I, R
        time_key
            Key label of the DataFrame which specifies the time points.
            Defaults to 'Time'.
        S_key
            Key label of the DataFrame which specifies S. Defaults to 'S'.
        E_key
            Key label of the DataFrame which specifies
            Key label of the DataFrame which specifies E. Defaults to 'E'.
        I_key
            Key label of the DataFrame which specifies
            Key label of the DataFrame which specifies I. Defaults to 'I'.
        R_key
            Key label of the DataFrame which specifies
            Key label of the DataFrame which specifies R. Defaults to 'R'.

        """

        # Plot of susceptibles
        self._fig.add_trace(
            go.Scatter(
                x=data[time_key],
                y=data[S_key],
                mode='lines',
                name='Susceptible'
            )
        )

        # Plot of exposed
        self._fig.add_trace(
            go.Scatter(
                x=data[time_key],
                y=data[E_key],
                mode='lines',
                name='Exposed'
            )
        )

        # Plot of infectious
        self._fig.add_trace(
            go.Scatter(
                x=data[time_key],
                y=data[I_key],
                mode='lines',
                name='Infectious'
            )
        )

        # Plot of Recovered
        self._fig.add_trace(
            go.Scatter(
                x=data[time_key],
                y=data[R_key],
                mode='lines',
                name='Recovered'
            )
        )

        # Update axis labels
        x_label = time_key
        y_label = 'Percentage in population'
        self._update_axis_labels(x_label, y_label)

    def _update_axis_labels(self, x_label, y_label):

        old_x_label = self._fig['layout']['xaxis']['title']['text']
        old_y_label = self._fig['layout']['yaxis']['title']['text']

        # Raise warning when the x axis label (time)
        # does not match the old one if it already exist;
        if (old_x_label is not None) and (old_x_label != x_label):
            warnings.warn(
                '''The time key does not match the previous time label.
                   The x label was set to the new time key,
                   but may no longer be appropriate for
                   the previously set data.''')

        # Raise warning when the y axis label (incidence)
        # does not match the old one if it already exist;
        if (old_y_label is not None) and (old_y_label != y_label):
            warnings.warn(
                '''The incidence key does not match the previous incidence label.
                   The y label was set to the new incidence key,
                   but may no longer be appropriate for
                   the previously set data.''')

        # Update axes
        self._fig.update_layout(
            xaxis_title=x_label,
            yaxis_title=y_label
        )

    def show(self):

        # Display the figure
        self._fig.show()
