import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    [
        html.I("Enter in the below boxes to fix the parameter values"),
        html.Br(),
        dcc.Input(id="Initial S", type="number", placeholder="Initial S"),
        dcc.Input(id="Initial E", type="number", placeholder="Initial E"),
        dcc.Input(id="Initial I", type="number", placeholder="Initial I"),
        dcc.Input(id="Initial R", type="number", placeholder="Initial R"),
        dcc.Input(
            id="Infection Rate", type="number", placeholder="Infection Rate"),
        dcc.Input(
            id="Incubation Rate", type="number", placeholder="Incubation Rate"),
        dcc.Input(
            id="Recovery Rate", type="number", placeholder="Recovery Rate"),
        html.Div(id="output"),
    ]
)


@app.callback(
    Output("output", "children"),
    Input("Initial S", "value"),
    Input("Initial E", "value"),
    Input("Initial I", "value"),
    Input("Initial R", "value"),
    Input("Infection Rate", "value"),
    Input("Incubation Rate", "value"),
    Input("Recovery Rate", "value"),
)
def update_output(S0, E0, I0, R0, beta, kappa, gamma):
    return u'Initial S = {}, Initial E = {}, Initial I = {}, Initial R = {}, Infection Rate = {}, Incubation Rate = {}, Recovery Rate = {}'.format(S0, E0, I0, R0, beta, kappa, gamma)

    name_value_dict = {'S0': S0, 'E0': E0, 'I0': I0, 'R0': R0, 'beta': beta, 'kappa': kappa, 'gamma': gamma}
    model.fix_parameters(name_value_dict)

if __name__ == "__main__":
    app.run_server(debug=True)
