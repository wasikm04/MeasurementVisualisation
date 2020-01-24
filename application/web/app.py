import firebase_admin
from firebase_admin import credentials
from callbacks import *
from visual.layout import *
import os

cred = credentials.Certificate(os.path.dirname(os.path.abspath(__file__)) + "/keys/measurementvisualisation-firebase-adminsdk-t9b3y-97539f3cd1.json")
firebase_admin.initialize_app(cred, {'databaseURL': 'https://measurementvisualisation.firebaseio.com'})

external_stylesheets = [dbc.themes.BOOTSTRAP]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config.suppress_callback_exceptions = True

app.layout = dbc.Container(
    children=[
        dcc.Store(id='store', storage_type='session'),
        generateNavbar(),
        generateBody(),
        dcc.Interval(
            id="interval-component", interval=1 * 2000, n_intervals=0  
        ),
        dcc.Interval(
            id="fetch-data", interval=1 * 2000, n_intervals=0  
        ),
    ],
    className="h-100",
    fluid=True
)
register_callbacks(app)

if __name__ == "__main__":
    app.run_server(debug=False)
