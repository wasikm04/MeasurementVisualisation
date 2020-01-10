from dash.dependencies import Input, Output, State

from firebase_db import save_patient_data
from layout import *
import json
import requests
import dash
import pandas as pd

#className={pretty_container}
def register_callbacks(app):

    @app.callback([Input("fetch-data", "n_intervals")])
    def download(value):
        data = json.dumps(fetchData(patient))
        #6 pobrań i zapis
        save_patient_data(patient, data)
        

    @app.callback(
        [
        Output("data-panel", "children"),
        Output("intermediate-valueLast", "children")
        ],
        [
            Input("intermediate-valueLive", "children"),
            Input("intermediate-valueButtons", "children"),
        ],
    )
    def updateVisualisation(value1, value2):
        ctx = dash.callback_context
        input_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if input_id == "intermediate-valueLive":
            data = json.loads(value1)
        elif input_id == "intermediate-valueButtons":
            data = json.loads(value2)
        return preparePanel(data), json.dumps(data)


    @app.callback(
        Output("intermediate-valueLive", "children"),
        [Input("interval-component", "n_intervals"),
         Input("patient-select", "value")],
    )
    def updateVisualisationLive(n_intervals, patient):
        data = get_last_patient_document(patient)
        return data


    @app.callback(
        [Output("graph", "figure"),
         Output("store", "data")],
        [Input("intermediate-valueLive", "children"),
         Input("patient-select", "value")],
        [State("store", "data")],
    )
    def updateGraph(patient, selectedPatient, data):
        data = data or {1: [], 2: [], 3: [], 4: [], 5: [], 6: []}
        newList = data[selectedPatient]
        if (len(listLen) >= 20):
            newList = newList.pop(0)
        newList = newList.append(json.loads(patient))
        data[selectedPatient] = newList
        # odjąć pierwszy i dodać nowego pateient do data odpowiedniego
        return composeGraph(data), data


    def composeGraph(dataList):
        return None


    @app.callback(
        [
            Output("current-action", "children"),
            Output("interval-component", "disabled"),
            Output("intermediate-valueButtons", "children"),
        ],
        [
            Input("prev-button", "n_clicks"),
            Input("next-button", "n_clicks"),
            Input("live-button", "n_clicks"),
            Input("stop-button", "n_clicks"),
            Input("next-anomaly-button", "n_clicks"),
            Input("prev-anomaly-button", "n_clicks"),
        ],
        [State("patient-select", "value"),
        State("intermediate-valueLast", "children")],
    )
    def manageButtons(prev, next, live, stop, next_anomaly, prev_anomaly, patient, data):
        ctx = dash.callback_context
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]
        data = json.loads(data)
        return prepareOutputBasedOnButton(button_id, patient, data)


def prepareOutputBasedOnButton(button_id, patient, data):
    #użycie id i timestamp z data do pobrania odpowiedniego dokumentu
    disable = True
    if button_id == "prev-button":
        message = "Visualisation shows previously fetched data"
    elif button_id == "next-button":
        message = "Visualisation shows next part of previously fetched data"
    elif button_id == "stop-button":
        message = "Visualisation is not updating, click 'Live'"
    elif button_id == "next-anomaly-button":
        message = "Visualisation shows next saved data with anomaly"
    elif button_id == "prev-anomaly-button":
        message = "Visualisation shows previous saved data with anomaly"
    elif button_id == "live-button":
        message = "Visualisation shows live updated data"
        disable = False
    else:
        disable = False

    return message, disable, data

