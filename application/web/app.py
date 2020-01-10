import dash
import dash_core_components as dcc
import dash_html_components as html
from callbacks import *
import dash_bootstrap_components as dbc
from layout import *
import firebase_admin
from firebase_admin import db, credentials, firestore

cred = credentials.Certificate("/keys/measurementvisualisation-firebase-adminsdk-t9b3y-97539f3cd1.json")
firebase_admin.initialize_app(cred, {'databaseURL': 'https://measurementvisualisation.firebaseio.com'})

external_stylesheets = [dbc.themes.BOOTSTRAP]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config.suppress_callback_exceptions = True

app.layout = dbc.Container(
    children=[
        generateNavbar(),
        generateBody(),
        dcc.Interval(
            id="interval-component", interval=1 * 1500, n_intervals=0  
        ),
    ],
    className="h-100",
    fluid=True
)
register_callbacks(app)

if __name__ == "__main__":
    #print('######################################')
    #database = firestore.client()
    #patient_col_ref = database.collection('patients')  # col_ref is CollectionReference
    #results = patient_col_ref.get()
    # results = col_ref.where('name', '==', 'Pepa').get()  # one way to query
    # results = col_ref.order_by('date', direction='DESCENDING').limit(
    #     1).get()  # another way - get the last document by date
    #for item in results:
    #    print(item.to_dict())
    #    print(item.id)
    app.run_server(debug=True)
