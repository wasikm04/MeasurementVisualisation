from dash.dependencies import Input, Output, State
from layout import *
import json
import requests
import dash

def register_callbacks(app):

    @app.callback(Output("data-panel", "children"),
                [Input('interval-component', 'n_intervals'),
                Input("patient-select", "value")])
    def updateVisualisationLive(n_intervals, patient):
        json = fetchData(patient)
        return preparePanel(json)

    @app.callback(
        [
            Output("current-action", "children"),
            Output('interval-component', 'disabled')
        ],
        [
            Input("prev-button", "n_clicks"),
            Input("next-button", "n_clicks"),
            Input("live-button", "n_clicks"),
            Input("stop-button", "n_clicks"),
            Input("next-anomaly-button", "n_clicks"),
            Input("prev-anomaly-button", "n_clicks")
        ])
    def manageButtons(prev, next, live, stop, next_anomaly, prev_anomaly):
        ctx = dash.callback_context
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        return prepareOutputBasedOnButton(button_id)
    

def prepareOutputBasedOnButton(button_id):
    message = ""
    disable = True
    if(button_id == "prev-button"):
        message = "Visualisation shows previously fetched data"
    elif(button_id == "next-button"):
        message = "Visualisation shows next part of previously fetched data"
    elif(button_id == "stop-button"):
        message = "Visualisation is not updating, click 'Live'"
    elif(button_id == "next-anomaly-button"):
        message = "Visualisation shows next saved data with anomaly"
    elif(button_id == "prev-anomaly-button"):
        message = "Visualisation shows previous saved data with anomaly"    
    elif(button_id == "live-button"):
        message = "Visualisation shows live updated data"
        disable=False
    else:
        disable = False
            
    return message, disable
    

    
