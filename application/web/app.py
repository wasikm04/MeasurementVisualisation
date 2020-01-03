import dash
import dash_core_components as dcc
import dash_html_components as html
from callbacks import *
import dash_bootstrap_components as dbc
from layout import *

external_stylesheets = [dbc.themes.BOOTSTRAP]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config.suppress_callback_exceptions = True

app.layout = dbc.Container(
    children=[
        generateNavbar(),
        generateBody(),
        dcc.Interval(
            id="interval-component", interval=1 * 10000, n_intervals=0  
        ),
    ],
    className="h-100",
    fluid=True
)
register_callbacks(app)

if __name__ == "__main__":
    app.run_server(debug=True)
