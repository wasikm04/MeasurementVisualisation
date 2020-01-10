from dash.dependencies import Input, Output, State

from firebase_db import save_patient_data, get_next_data, get_previous_data, get_next_anomaly, get_previous_anomaly
from layout import *
import json
import requests
import dash
import pandas as pd

def register_callbacks(app):

    @app.callback(Output("data-panel", "children"),
                [Input('intermediate-value1', 'children'),
                Input("intermediate-value2", "children")])
    def updateVisualisation(value1, value2):
        ctx = dash.callback_context
        input_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if(input_id == "intermediate-value1"): 
            data = json.loads(value1)
        elif(input_id == "intermediate-value2"):
            data = json.loads(value2)
        return preparePanel(data)


    @app.callback(Output("intermediate-value1", "children"),
                [Input('interval-component', 'n_intervals'),
                Input("patient-select", "value")])
    def updateVisualisationLive(n_intervals, patient):
        data = json.dumps(fetchData(patient))
        save_patient_data(patient, data)
        return data


    @app.callback(
        [
            Output("current-action", "children"),
            Output('interval-component', 'disabled'),
            Output("intermediate-value2", "children")
        ],
        [
            Input("prev-button", "n_clicks"),
            Input("next-button", "n_clicks"),
            Input("live-button", "n_clicks"),
            Input("stop-button", "n_clicks"),
            Input("next-anomaly-button", "n_clicks"),
            Input("prev-anomaly-button", "n_clicks")
        ],
        [State("patient-select", "value")])
    def manageButtons(prev, next, live, stop, next_anomaly, prev_anomaly, patient):
        ctx = dash.callback_context
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        return prepareOutputBasedOnButton(button_id, patient)
    

def prepareOutputBasedOnButton(button_id, patient):
    # Przykładowe wykorzystanie, tu kolejny strzał do api ale powinno być pobranie z bazy/ local storage w zależności jak akcja
    data = json.dumps(fetchData(patient))
    #
    disable = True
    if(button_id == "prev-button"):
        # data = get_prevoius_data(patient, time)
        message = "Visualisation shows previously fetched data"
    elif(button_id == "next-button"):
        # data = get_next_data(patient, time)
        message = "Visualisation shows next part of previously fetched data"
    elif(button_id == "stop-button"):
        message = "Visualisation is not updating, click 'Live'"
    elif(button_id == "next-anomaly-button"):
        # data = get_next_anomaly(patient, time)
        message = "Visualisation shows next saved data with anomaly"
    elif(button_id == "prev-anomaly-button"):
        # data = get_previous_anomaly(patient, time)
        message = "Visualisation shows previous saved data with anomaly"    
    elif(button_id == "live-button"):
        message = "Visualisation shows live updated data"
        disable=False
    else:
        disable = False
            
    return message, disable, data
    

    
