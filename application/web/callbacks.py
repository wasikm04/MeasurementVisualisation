from dash.dependencies import Input, Output, State
from layout import *
import json
import requests

def register_callbacks(app):
# @app.callback(
#     Output("data-panel", "children"),
#     [Input("patient-select", "value")],
# )
# def choosePatient(patient):
#     json = fetchData(patient)
#     return preparePanel(json)

    @app.callback(Output("data-panel", "children"),
                [Input('interval-component', 'n_intervals'),
                Input("patient-select", "value")])
    def updateVisualisationLive(n_intervals, patient):
        json = fetchData(patient)
        return preparePanel(json)
