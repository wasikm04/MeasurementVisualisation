from dash.dependencies import Input, Output, State

from firebase_db import save_patient_data
from layout import *
import json
import requests
import dash
import pandas as pd


def register_callbacks(app):
    @app.callback(
        Output("data-panel", "children"),
        [
            Input("intermediate-value1", "children"),
            Input("intermediate-value2", "children"),
        ],
    )
    def updateVisualisation(value1, value2):
        ctx = dash.callback_context
        input_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if input_id == "intermediate-value1":
            data = json.loads(value1)
        elif input_id == "intermediate-value2":
            data = json.loads(value2)
        return preparePanel(data)

    @app.callback(
        Output("intermediate-value1", "children"),
        [Input("interval-component", "n_intervals"), Input("patient-select", "value")],
    )
    def updateVisualisationLive(n_intervals, patient):
        data = json.dumps(fetchData(patient))
        save_patient_data(patient, data)
        return data

    @app.callback(
        [Output("graph", "figure"), Output("store", "data")],
        [Input("intermediate-value1", "children"),
         Input("patient-select", "value")],
        [State("store", "data")],
    )
    def updateGraph(patient, selectedPatient, data):
        data = data or {1: [], 2: [], 3: [], 4: [], 5: [], 6: []}
        newList = data[selectedPatient]
        if (len(listLen) >= 20):
            newList = newList.pop(0)
        newList = newList.append(patient)
        data[selectedPatient] = newList
        # odjąć pierwszy i dodać nowego pateient do data odpowiedniego
        return composeGraph(data), data


    def composeGraph(dataList):
        return None


    @app.callback(
        [
            Output("current-action", "children"),
            Output("interval-component", "disabled"),
            Output("intermediate-value2", "children"),
        ],
        [
            Input("prev-button", "n_clicks"),
            Input("next-button", "n_clicks"),
            Input("live-button", "n_clicks"),
            Input("stop-button", "n_clicks"),
            Input("next-anomaly-button", "n_clicks"),
            Input("prev-anomaly-button", "n_clicks"),
        ],
        [State("patient-select", "value")],
    )
    def manageButtons(prev, next, live, stop, next_anomaly, prev_anomaly, patient):
        ctx = dash.callback_context
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]
        return prepareOutputBasedOnButton(button_id, patient)


def prepareOutputBasedOnButton(button_id, patient):
    # Przykładowe wykorzystanie, tu kolejny strzał do api ale powinno być pobranie z bazy/ local storage w zależności jak akcja
    data = json.dumps(fetchData(patient))
    #
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

