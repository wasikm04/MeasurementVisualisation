from dash.dependencies import Input, Output, State
from firebase_db import save_patient_data, get_next_data, get_previous_data, get_next_anomaly, get_previous_anomaly,get_all_patient_documents, get_last_patient_document, save_many_patients_data
from layout import *
from helper import *
import json
import requests
import dash
import pandas as pd
import plotly
from datetime import datetime
import plotly.graph_objs as go

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
        #data = get_last_patient_document(int(patient)) pobieranie z bazy zakomentowane
        data = fetchData(patient)
        print(str(datetime.fromtimestamp(data.get("timestamp"))))
       # return json.dumps(data[0])
        return json.dumps(data)

    @app.callback(
        [Output("graph", "figure"),
         Output("store", "data")],
        [Input("intermediate-valueLive", "children"),
         Input("patient-select", "value")],
        [State("store", "data")],
    )
    def updateGraph(patient, selectedPatient, data):
        data = data or {'1': [], '2': [], '3': [], '4': [], '5': [], '6': []}
        newList = data[str(selectedPatient)]
        if (len(newList) >= 6):
            newList.pop(0)
        newList.append(json.loads(patient))
        data[str(selectedPatient)] = newList
        return composeGraph(newList), data
    
    def composeGraph(dataList):
        layout_graph = layout
        xList, yList = produceData(dataList)
        data = prepareGraphData(xList, yList)
        
        layout_graph["xaxis"] = dict(range=[min(xList),max(xList)])
        layout_graph["yaxis"] = dict(range=[min(min(yList))-30,max(max(yList))+30])
        layout_graph["transition"] = {
               'duration': 500,
               'easing': 'linear-in-out',
               "ordering": 'traces first'
           }
        # layout_graph = go.Layout(xaxis = dict(range=[min(xList),max(xList)]),
        #     yaxis = dict(range=[min(min(yList))-30,max(max(yList))+30]))
        return {'data': data,'layout' : layout_graph}

    def produceData(dataList):
        xList = []
        tmp = dict([(0,[]),(1,[]),(2,[]),(3,[]),(4,[]),(5,[])])
        for obj in dataList:
            xList.append(str(datetime.fromtimestamp(obj.get("timestamp"))).split(" ")[1].split(".")[0])
            data = obj.get("trace").get("sensors")
            for val in data:
                tmp[val.get("id")].append(val.get("value"))

        return xList, [tmp[0],tmp[1],tmp[2],tmp[3],tmp[4],tmp[5]]

    def prepareGraphData(xList, yList):
        data = []
        for x in range(6):
            line = dict(
                type="scatter",
                mode="lines+markers",
                name="Sensor " + str(x),
                x=xList,
                y=yList[x],
                line=dict(shape="spline", color=colors[x]), 
                marker=dict(symbol="diamond") #, line={"color": colors[x]})
            )
            data.append(line)
        return data    

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
        if(button_id == "prev-button"):
            data = get_previous_data(patientId, patientData.get("timestamp"))[0]
            message = "Visualisation shows previously fetched data"
        elif(button_id == "next-button"):
            data = get_next_data(patientId, patientData.get("timestamp"))[0]
            message = "Visualisation shows next part of previously fetched data"
        elif button_id == "stop-button":
            message = "Visualisation is not updating, click 'Live'"
        elif(button_id == "next-anomaly-button"):
            data = get_next_anomaly(patientId, patientData.get("timestamp"))
            message = "Visualisation shows next saved data with anomaly"
        elif(button_id == "prev-anomaly-button"):
            data = get_previous_anomaly(patientId, patientData.get("timestamp"))
            message = "Visualisation shows previous saved data with anomaly"    
        elif(button_id == "live-button"):
            message = "Visualisation shows live updated data"
            disable = False

        if data == {} or data == []:
            data = patientData

        return message, disable, json.dumps(data)


    mapbox_access_token = "pk.eyJ1IjoiamFja2x1byIsImEiOiJjajNlcnh3MzEwMHZtMzNueGw3NWw5ZXF5In0.fk8k06T96Ml9CLGgKmk81w"
    layout = dict(
        autosize=True,
        automargin=True,
        margin=dict(l=30, r=30, b=20, t=40),
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

    colors = dict([(0,"#59C3C3"),(1,"#08ffff"),(2,"#626666"),(3,"#82e81c"),(4,"#70a13f"),(5,"#518c15")])