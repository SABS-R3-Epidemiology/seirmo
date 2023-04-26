#
# This file is part of seirmo (https://github.com/SABS-R3-Epidemiology/seirmo/)
# which is released under the BSD 3-clause license. See accompanying LICENSE.md
# for copyright notice and full license details.
#

from plotly.subplots import make_subplots
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
            A pandas.DataFrame including two columns, one being time points,
            the other being incidence number.
        time_key
            Key label of the DataFrame which specifies the time points.
            Defaults to 'Time'.
        inc_key
            Key label of the DataFrame which specifies the
            incidence number. Defaults to 'Incidence Number'.

        """
        # Plot a bar chart for the data
        self._fig.add_trace(
            go.Bar(
                x=data[time_key],
                y=data[inc_key],
                name='cases',
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
            A pandas.DataFrame including two columns, one being time points,
            the other being incidence number.
        time_key
            Key label of the DataFrame which specifies the time points.
            Defaults to 'Time'.
        inc_key
            Key label of the DataFrame which specifies
            the incidence number. Defaults to 'Incidence Number'.

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
                '''The incidence key does not match the previous incidence
                   label. The y label was set to the new incidence key,
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

    def add_simulation(
        self, data, time_key='Time',
        compartment_keys=[
            'Susceptible', 'Exposed', 'Infectious', 'Recovered']):

        """

        Add line plot traces for the simulated compartment numbers
        in the figure

        Parameters
        ----------
        data
            A pandas.DataFrame including columns
            for time points and compartment numbers
        time_key
            Key label of the DataFrame which specifies the time points.
            Defaults to 'Time'.
        compartment_keys
            The list of key labels of the DataFrame
            which specify the compartments.
            Defaults to ['Susceptible', 'Exposed', 'Infectious', 'Recovered'].

        """

        # Line plots of the compartments
        for compartment_key in compartment_keys:
            self._fig.add_trace(
                go.Scatter(
                    x=data[time_key],
                    y=data[compartment_key],
                    mode='lines',
                    name=compartment_key
                )
            )

        # Update axis labels
        x_label = time_key
        y_label = 'Number of individuals'
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
                '''The incidence key does not match the previous incidence
                   label. The y label was set to the new incidence key,
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


class SubplotFigure(object):
    """

    A class that creates a figure consisting of subplots for
    IncidenceNumberPlot and CompartmentPlot.

    """
    def __init__(self):
        super(SubplotFigure, self).__init__()

        self._incidence_num_plot = IncidenceNumberPlot()
        self._compartment_plot = CompartmentPlot()

        self._fig = make_subplots(rows=2, cols=1)

    def _get_layout(self):
        """

        Get the layout from the IncidenceNumberPlot and CompartmentPlot
        and set the labels of the subplots

        """

        # Get the layout from IncidenceNumberPlot
        self._fig.update_xaxes(
            title_text=self._incidence_num_plot._fig['layout']['xaxis']['title']['text'], # noqa
            row=1, col=1)
        self._fig.update_yaxes(
            title_text=self._incidence_num_plot._fig['layout']['yaxis']['title']['text'], # noqa
            row=1, col=1)

        # Get the layout from CompartmentPlot
        self._fig.update_xaxes(
            title_text=self._compartment_plot._fig['layout']['xaxis']['title']['text'], # noqa
            row=2, col=1)
        self._fig.update_yaxes(
            title_text=self._compartment_plot._fig['layout']['yaxis']['title']['text'], # noqa
            row=2, col=1)

    def _get_trace(self):
        """

        Get the traces from the IncidenceNumberPlot and CompartmentPlot
        and add them to the subplots

        """

        # Get the traces from the IncidenceNumberPlot
        # Count the number of traces in IncidenceNumberPlot
        num1 = len(self._incidence_num_plot._fig['data'])

        # Get the traces
        for i in range(num1):
            self._fig.add_trace(
                go.Bar(
                    x=self._incidence_num_plot._fig['data'][i]['x'],
                    y=self._incidence_num_plot._fig['data'][i]['y'],
                    name=self._incidence_num_plot._fig['data'][i]['name']),
                row=1, col=1
            )

        # Get the traces from the CompartmentPlot
        # Count the number of traces in CompartmentPlot
        num2 = len(self._compartment_plot._fig['data'])

        # Get the traces
        for i in range(num2):
            self._fig.add_trace(
                go.Scatter(
                    x=self._compartment_plot._fig['data'][i]['x'],
                    y=self._compartment_plot._fig['data'][i]['y'],
                    mode='lines',
                    name=self._compartment_plot._fig['data'][i]['name']),
                row=2, col=1
            )

    def add_data(self, data, time_key='Time',
                 inc_key='Incidence Number'):
        """

        Add a bar plot trace for the given incidence number data
        in the bar subplot

        Parameters
        ----------
        data
            A pandas.DataFrame including two columns, one being time points,
            the other being incidence number.
        time_key
            Key label of the DataFrame which specifies the time points.
            Defaults to 'Time'.
        inc_key
            Key label of the DataFrame which specifies
            the incidence number. Defaults to 'Incidence Number'.

        """

        # Plot a bar chart for the incidence number data in the subplot
        self._incidence_num_plot.add_data(
            data, time_key=time_key, inc_key=inc_key)

    def add_simulation(
        self, data, time_key='Time', inc_key='Incidence Number',
        compartment_keys=[
            'Susceptible', 'Exposed', 'Infectious', 'Recovered']):
        """

        Add a bar plot trace for the simulated incidence numbers
        in the first subplot,
        and add line plot traces for the simulated compartment numbers
        in the second subplot.

        Parameters
        ----------
        data
            A pandas.DataFrame including columns
            for time points, incidence number, compartment numbers
        time_key
            Key label of the DataFrame which specifies the time points.
            Defaults to 'Time'.
        inc_key
            Key label of the DataFrame which specifies
            the incidence number. Defaults to 'Incidence Number'.
        compartment_keys
            The list of key labels of the DataFrame
            which specify the compartments.
            Defaults to ['Susceptible', 'Exposed', 'Infectious', 'Recovered'].

        """

        # Plot a bar chart for the simulated incidence number
        # in the first subplot
        self._incidence_num_plot.add_simulation(
            data, time_key=time_key, inc_key=inc_key)

        # Add line plot traces for the simulated compartment numbers
        # in the second subplot
        self._compartment_plot.add_simulation(
            data, time_key=time_key, compartment_keys=compartment_keys)

    def get_subplots(self):
        """

        Get the traces and layout into the subplots

        """

        self._get_layout()
        self._get_trace()

    def show(self):
        """

        Display the figure

        """

        self._fig.show()
