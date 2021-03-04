#
# This file is part of seirmo (https://github.com/SABS-R3-Epidemiology/seirmo/)
# which is released under the BSD 3-clause license. See accompanying LICENSE.md
# for copyright notice and full license details.
#

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
import pints

import seirmo as se
from seirmo import plots


class _OptimisationApp(object):
    """SimulationApp Class:

    Creates the SEIR model simulation app.

    """

    def __init__(self):
        super(_OptimisationApp, self).__init__()

        self.params = [
            'Initial S', 'Initial E', 'Initial I', 'Initial R',
            'Infection Rate', 'Incubation Rate', 'Recovery Rate'
        ]

        self._subplot_fig = plots.SubplotFigure()
        self._inferred_params_table = []

        self.simulation_start = 0
        self.simulation_end = 30

    def _set_layout(self):
        """
        Create the layout of the app.
        """

        self.app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
        self._subplot_fig._fig['layout']['legend']['uirevision'] = True

        self.app.layout = dbc.Container([
            dbc.Row([
                    dbc.Col(
                        [dcc.Graph(
                            figure=self._subplot_fig._fig, id='fig',
                            style={'height': '80vh'}),
                            dash_table.DataTable(
                            id='inferred-parameters-table',
                            columns=(
                                [{'id': 'Run', 'name': 'Run'}] +
                                [{'id': p, 'name': p} for p in self.params]
                            ),
                            data=self._inferred_params_table)],
                        md=9),
                    dbc.Col([
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.Button('Run', id='run-button', n_clicks=0),
                        dcc.Loading(
                            id="loading-1",
                            type="default",
                            children=html.Div(id="loading-output-1")),
                        html.Button('Reset', id='reset-button', n_clicks=0),
                        html.Br(),
                        html.Br(),
                        html.I("Enter in the below boxes to fix the parameter values"), # noqa
                        html.Br(),
                        dcc.Input(
                            id="Initial S",
                            type="number",
                            placeholder="Initial S"),
                        dcc.Input(
                            id="Initial E",
                            type="number",
                            placeholder="Initial E"),
                        dcc.Input(
                            id="Initial I",
                            type="number",
                            placeholder="Initial I"),
                        dcc.Input(
                            id="Initial R",
                            type="number",
                            placeholder="Initial R"),
                        dcc.Input(
                            id="Infection Rate",
                            type="number",
                            placeholder="Infection Rate"),
                        dcc.Input(
                            id="Incubation Rate",
                            type="number",
                            placeholder="Incubation Rate"),
                        dcc.Input(
                            id="Recovery Rate",
                            type="number",
                            placeholder="Recovery Rate"),
                        html.Div(id="fixed-parameters-output"),
                    ], md=3)
                    ])
        ], fluid=True)

    def add_data(self, data, time_key='Time', inc_key='Incidence Number'):
        """
        Plot subplot for the given incidence number data.

        Parameters
        ----------
        data
            A pandas.DataFrame with 2 columns, one being time points,
            the other being incidence number.
        time_key
            Key label of the DataFrame which specifies the time points.
            Defaults to 'Time'.
        inc_key
            Key label of the DataFrame which specifies the
            incidence number.
            Defaults to 'Incidence Number'.
        """

        if not isinstance(data, pd.DataFrame):
            raise TypeError(
                'Data has to be an instance of pandas.DataFrame.')

        if time_key not in data.columns:
            raise ValueError(
                'The input time key does not match that in the data.')

        if inc_key not in data.columns:
            raise ValueError(
                'The input incidence key does not match that in the data.')

        self._subplot_fig.add_data(
            data, time_key, inc_key)

    def add_model(self, model, parameters_name):
        """
        Plot subplots of simulation for the given model.

        Parameters
        ----------
        model
            A subclass of seirmo.ForwardModel class, which specifies
            the model of simulation.
        parameters_name
            Name of parameters of model in list of strings.
        """

        parameters_name = list(parameters_name)

        init_parameters = []

        for model_parameter in parameters_name:
            model_parameter = str(model_parameter)
            self._slider_component.add_slider(
                slider_id=model_parameter,
                min_value=0,
                max_value=1,
                initial_value=0.5)
            init_parameters.append(
                self._slider_component._sliders[model_parameter].children[1].value) # noqa

        self._slider_component.group_sliders(
            parameters_name, 'Sliders of parameters')

        self.simulate = se.SimulationController(
            model, self.simulation_start, self.simulation_end)

        data = self.simulate.run(init_parameters)
        data = pd.DataFrame({
            'Time': list(self.simulate._simulation_times),
            'Incidence Number': data[:, -1],
            'Susceptible': data[:, 0],
            'Exposed': data[:, 1],
            'Infectious': data[:, 2],
            'Recovered': data[:, 3],
        })

        self._subplot_fig.add_simulation(data)

    def add_problem(self, data, model):
        # Check model is ForwardModel
        if not issubclass(model, se.ForwardModel):
            raise TypeError(
                'Model has to be a subclass of seirmo.ForwardModel.')

        time_key = 'Time'
        inc_key = 'Incidence Number'
        # Visualise data
        self.data = data
        self._subplot_fig.add_data(
            self.data, time_key, inc_key)

        self.simulate = se.SimulationController(
            model, self.simulation_start, self.simulation_end)

        initialise_data = pd.DataFrame({
            'Time': [0],
            'Incidence Number': [0],
            'Susceptible': [0],
            'Exposed': [0],
            'Infectious': [0],
            'Recovered': [0],
        })

        self._subplot_fig.add_simulation(initialise_data)

        # Create model
        model = model()
        model = se.SEIRModel()
        model.set_outputs(['Incidence'])
        self.model = se.ReducedModel(model)

    def get_subplots(self):
        self._subplot_fig.get_subplots()

    def slider_ids(self):
        """
        Return the ids of sliders added to the app.
        """
        return self._slider_component.get_slider_ids()

    def set_prior(self, name_value_dict):
        """
        Organise the priors for free parameters.

        The priors are pre-tested separately.

        Parameters
        ----------
        name_value_dict
            Dictionary of fixed parameters with their values.
        """
        prior_list = [pints.UniformLogPrior(0, 100),
                      pints.UniformLogPrior(0, 10),
                      pints.UniformLogPrior(0, 10),
                      pints.UniformLogPrior(0, 100),
                      pints.UniformLogPrior(0, 1),
                      pints.UniformLogPrior(0, 1),
                      pints.UniformLogPrior(0, 1)]
        prior_dict = {name: value for (name, value) in zip(
            self.model._parameter_names, prior_list)}

        priors = []
        for key in name_value_dict:
            if name_value_dict[key] is None:
                priors.append(prior_dict[key])

        priors.append(pints.UniformLogPrior(0, 1))

        return priors

    def update_model(self, fixed_parameters_list):
        """
        Update the model with fixed parameters.

        Parameters
        ----------
        fixed_parameters_list
            List of fixed parameter values.
        """

        # Create dictionary of fixed parameters and its values
        name_value_dict = {name: value for (name, value) in zip(
            self.model._parameter_names, fixed_parameters_list)}
        self.model.fix_parameters(name_value_dict)

        # Setup the problem with pints,
        # including likelihood, prior and posterior
        print(self.model.n_parameters())
        problem = pints.SingleOutputProblem(
            model=self.model,
            times=self.data['Time'].to_numpy(),
            values=self.data['Incidence Number'].to_numpy())
        log_likelihood = pints.GaussianLogLikelihood(problem)
        priors = self.set_prior(name_value_dict)
        self.log_prior = pints.ComposedLogPrior(*priors)
        self.log_posterior = pints.LogPosterior(log_likelihood, self.log_prior)

        # Run transformation
        self.transformations = pints.LogTransformation(
            self.log_posterior.n_parameters())

    def reset(self):
        """
        Reset the app
        """

        for i in range(5):
            self._subplot_fig._fig['data'][i + 1]['x'] = [0]
            self._subplot_fig._fig['data'][i + 1]['y'] = [0]

        self._inferred_params_table = []

        return self._subplot_fig._fig, self._inferred_params_table

    def update_simulation(self, n_clicks):
        """
        Update the subplots with simulated data of new parameters.

        Parameters
        ----------
        n_clicks
            Number of 'Run' button clicks.
        """
        if n_clicks == 0:
            return self._subplot_fig._fig, self._inferred_params_table
        else:
            # Set up optimisation controller
            initial_parameters = self.log_prior.sample()
            opt = pints.OptimisationController(
                function=self.log_posterior,
                x0=initial_parameters,
                method=pints.CMAES,
                transform=self.transformations)
            opt.set_parallel(True)
            opt.set_log_to_screen(False)
            parameters, _ = opt.run()

            # Organise free parameters and fixed parameters for simulation
            full_params_value = self.model._fixed_params_values
            if full_params_value is None:
                full_params_value = parameters[:-1]
            else:
                count = 0
                for i in range(int(
                        self.model.n_parameters()
                        + self.model.n_fixed_parameters())):

                    if self.model._fixed_params_mask[i] == 0:
                        full_params_value[i] = parameters[count]
                        count += 1

            data = self.simulate.run(full_params_value)

            # Update figure with simulation from inferred parameters
            # Update times (x values)
            for i in range(5):
                self._subplot_fig._fig['data'][i + 1]['x'] = list(
                    self.simulate._simulation_times)

            # Update y values
            self._subplot_fig._fig['data'][1]['y'] = data[:, 4]
            self._subplot_fig._fig['data'][2]['y'] = data[:, 0]
            self._subplot_fig._fig['data'][3]['y'] = data[:, 1]
            self._subplot_fig._fig['data'][4]['y'] = data[:, 2]
            self._subplot_fig._fig['data'][5]['y'] = data[:, 3]

            # Update table with inferred parameters
            inferred_params_dict = dict(
                Run=len(self._inferred_params_table) + 1,
                    **{param: round(value, 3) for (param, value) in zip(
                        self.params, full_params_value)})

            self._inferred_params_table.append(inferred_params_dict)

            return self._subplot_fig._fig, self._inferred_params_table
