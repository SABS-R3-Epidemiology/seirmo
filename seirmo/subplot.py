#
# This file is part of seirmo (https://github.com/SABS-R3-Epidemiology/seirmo/)
# which is released under the BSD 3-clause license. See accompanying LICENSE.md
# for copyright notice and full license details.
#

from plotly.subplots import make_subplots
import plotly.graph_objects as go
import warnings

import seirmo as se


class SubplotFigure(object):
    """

    A class that creates a figure consisting of subplots for
    IncidenceNumberPlot and CompartmentPlot.

    """
    def __init__(self):
        super(SubplotFigure, self).__init__()

        self._incidence_num_plot = se.IncidenceNumberPlot()
        self._compartment_plot = se.CompartmentPlot()

        self._fig = make_subplots(rows=2, cols=1)

    def _get_layout(self):
        """

        Get the layout from the IncidenceNumberPlot and CompartmentPlot
        and set the labels of the subplots

        """

        # Get the layout from IncidenceNumberPlot
        self._fig.update_xaxes(
            title_text=self._incidence_num_plot._fig['layout']['xaxis']['title']['text'],
            row=1, col=1)
        self._fig.update_yaxes(
            title_text=self._incidence_num_plot._fig['layout']['yaxis']['title']['text'],
            row=1, col=1)
        
        # Get the layout from CompartmentPlot
        self._fig.update_xaxes(
            title_text=self._compartment_plot._fig['layout']['xaxis']['title']['text'],
            row=2, col=1)
        self._fig.update_yaxes(
            title_text=self._compartment_plot._fig['layout']['yaxis']['title']['text'],
            row=2, col=1)


    def _get_trace(self)
        """

        Get the traces from the IncidenceNumberPlot and CompartmentPlot
        and add them to the subplots

        """

        # Get the traces from the IncidenceNumberPlot
        # Count the number of traces in IncidenceNumberPlot
        num1 = len(self._incidence_num_plot._fig['data'])

        # Get the traces
        for i in range(num1)
        self._fig.add_trace(
            go.Bar(
                x=self._incidence_num_plot._fig['data'][i]['x'],
                y=self._incidence_num_plot._fig['data'][i]['y'],
                name=self._incidence_num_plot._fig['data'][i]['name'],
                row=1, col=1
            )
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
                    name=self._compartment_plot._fig['data'][i]['name']
                    row=2, col=1
                )
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
            the incididence number. Defaults to 'Incidence Number'.

        """

        # Plot a bar chart for the incidence number data in the subplot
        self._incidence_num_plot.add_data(
            data, time_key=time_key, inc_key=inc_key)

        # Get the layout and trace into the subplot
        self._get_layout
        self._get_trace

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
            the incididence number. Defaults to 'Incidence Number'.
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

        # Get the layout and traces into the subplots
        self._get_layout
        self._get_trace

    def show(self):

        # Display the figure
        self._fig.show()
