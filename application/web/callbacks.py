from dash.dependencies import Input, Output, State
from firebase_db import save_patient_data, get_next_data, get_previous_data, get_next_anomaly, get_previous_anomaly,get_all_patient_documents, get_last_patient_document, save_many_patients_data
from layout import *
import json
import requests
import dash
import pandas as pd

#className={pretty_container}
def register_callbacks(app):

    @app.callback(Output("placeholder", "children"),
                [Input("fetch-data", "n_intervals")])
    def download(value):
        data = []
        for i in range(1,7):
            patient = fetchData(i)
            data.append(patient)
        save_many_patients_data(data)
        return ""


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
        data3 = get_last_patient_document(1)
        print("\n\n\n")
        print(data3)
        print("\n\n\n")
        data4 = get_last_patient_document(2)
        print("\n\n\n")
        return json.dumps(data[0])

    # @app.callback(
    #     [Output("graph", "figure"),
    #      Output("store", "data")],
    #     [Input("intermediate-valueLive", "children"),
    #      Input("patient-select", "value")],
    #     [State("store", "data")],
    # )
    # def updateGraph(patient, selectedPatient, data):
    #     data = data or {1: [], 2: [], 3: [], 4: [], 5: [], 6: []}
    #     newList = data[selectedPatient]
    #     if (len(listLen) >= 20):
    #         newList = newList.pop(0)
    #     newList = newList.append(json.loads(patient))
    #     data[selectedPatient] = newList
    #     return composeGraph(data), data
    #
    # def composeGraph(dataList):
    #     return None

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
        if data != None:
            data = json.loads(data)
        return prepareOutputBasedOnButton(button_id, patient, data)



    def prepareOutputBasedOnButton(button_id, patientId, patientData):
        #użycie patientDd i timestamp z patientData do pobrania odpowiedniego dokumentu
        disable = True
        if(button_id == "prev-button"):
            # data = get_prevoius_data(patient, time)
            message = "Visualisation shows previously fetched data"
        elif(button_id == "next-button"):
            # data = get_next_data(patient, time)
            message = "Visualisation shows next part of previously fetched data"
        elif button_id == "stop-button":
            message = "Visualisation is not updating, click 'Live'"
        elif(button_id == "next-anomaly-button"):
            # data = get_next_anomaly(patient, time)
            message = "Visualisation shows next saved data with anomaly"
        elif(button_id == "prev-anomaly-button"):
            # data = get_previous_anomaly(patient, time)
            message = "Visualisation shows previous saved data with anomaly"    
        elif(button_id == "live-button"):
            message = "Visualisation shows live updated data"
            disable = False
        else:
            disable = False

        return message, disable, json.dumps(patientData)

