from dash.dependencies import Input, Output, State
from firebase_db import get_next_data, get_previous_data, get_next_anomaly, get_previous_anomaly, \
    save_many_patients_data
from visual.layout import *
from helper import *
import json
import dash
from datetime import datetime
from graph_helper import composeGraph

def register_callbacks(app):
    @app.callback(Output("placeholder", "children"),
                  [Input("fetch-data", "n_intervals")])
    def download(value):
        data = []
        for i in range(1, 7):
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
            Input("intermediate-valueSlider", "children"),
        ],
    )
    def updateVisualisation(value1, value2, value3):
        ctx = dash.callback_context
        input_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if input_id == "intermediate-valueLive":
            data = json.loads(value1)
        elif input_id == "intermediate-valueButtons":
            data = json.loads(value2)
        elif input_id == "intermediate-valueSlider":
            data = json.loads(value3)
        return preparePanel(data), json.dumps(data)

    @app.callback(
        Output("intermediate-valueLive", "children"),
        [Input("interval-component", "n_intervals"),
         Input("patient-select", "value")],
    )
    def updateVisualisationLive(n_intervals, patient):
        data = fetchData(patient)
        print(str(datetime.fromtimestamp(data.get("timestamp"))))
        return json.dumps(data)

    @app.callback(
        [Output("graph", "figure"),
         Output("store", "data")],
        [Input("intermediate-valueLive", "children"),
         Input("intermediate-valueButtons", "children"),
         Input("clear-button", "n_clicks"),
         Input("patient-select", "value")],
        [State("store", "data")],
    )
    def updateGraph(patientLive, patientButton, clear, selectedPatient, data):
        empty = {'1': [], '2': [], '3': [], '4': [], '5': [], '6': []}
        data = data or empty
        newList = data[str(selectedPatient)]

        ctx = dash.callback_context
        input_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if input_id == "intermediate-valueLive":
            if (len(newList) >= 6):
                newList.pop(0)
            newList.append(json.loads(patientLive))
        elif input_id == "intermediate-valueButtons":
            if json and json.loads(patientButton) and json.loads(patientLive):
                if json.loads(patientButton).get("timestamp") != json.loads(patientLive).get("timestamp"):
                    if (len(newList) >= 6):
                        newList.pop(0)
                    newList.append(json.loads(patientButton))
        elif input_id == "clear-button":
            return {'data': [], 'layout': layout}, empty

        data[str(selectedPatient)] = newList
        return composeGraph(newList), data

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
        else:
            button_id = "live-button"
        return prepareOutputBasedOnButton(button_id, int(patient), data)

    def prepareOutputBasedOnButton(button_id, patientId, patientData):
        disable = True
        data = {}
        if (button_id == "prev-button"):
            data = get_previous_data(patientId, patientData.get("timestamp"))[0]
            message = "Visualisation shows previously fetched data"
        elif (button_id == "next-button"):
            data = get_next_data(patientId, patientData.get("timestamp"))
            if len(data) >= 1:
                data = data[0]
            message = "Visualisation shows next part of previously fetched data"
        elif button_id == "stop-button":
            message = "Visualisation is not updating, click 'Live'"
        elif (button_id == "next-anomaly-button"):
            data = get_next_anomaly(patientId, patientData.get("timestamp"))
            message = "Visualisation shows next saved data with anomaly"
        elif (button_id == "prev-anomaly-button"):
            data = get_previous_anomaly(patientId, patientData.get("timestamp"))
            message = "Visualisation shows previous saved data with anomaly"
        elif (button_id == "live-button"):
            message = "Visualisation shows live updated data"
            disable = False

        if data == {} or data == []:
            data = patientData

        return message, disable, json.dumps(data)

    @app.callback(
        [Output('text-slider', 'children'),
         Output('intermediate-valueSlider', 'children')],
        [Input('timestamp-slider', 'value')],
        [State("patient-select", "value")])
    def update_slider(value, patientId):
        newTime = time.time() - (10.1 - value) / 10.0 * 600
        newData = get_previous_data(int(patientId), newTime)[0]
        return '{}'.format(str(datetime.fromtimestamp(newData.get("timestamp"))).split(".")[0]), json.dumps(newData)



layout = dict(
        # autosize=True,
        # automargin=True,
        # margin=dict(l=30, r=30, b=20, t=40),
        hovermode="closest",
        plot_bgcolor="#F9F9F9",
        paper_bgcolor="#F9F9F9",
        legend=dict(font=dict(size=13), orientation="h"),
        title="Pressure Overview",
        #  mapbox=dict(
        #     accesstoken=mapbox_access_token,
        #      style="light",
        #      center=dict(lon=-78.05, lat=42.54),
        #      zoom=7,
        #  ),
    )

colors = dict([(0, "#59C3C3"), (1, "#08ffff"), (2, "#626666"), (3, "#82e81c"), (4, "#70a13f"), (5, "#518c15")])