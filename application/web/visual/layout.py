import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from datetime import datetime
from helper import *
from visual.controls_panel import generateControls
from visual.sensors_panel import updateData


def generateNavbar():
    return dbc.NavbarSimple(brand="Medical Data Visualisation")



def generateBody():
    return html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.H2(
                                "Controller",
                                style={"textAlign": "center", "justify": "center"},
                            ),
                            dbc.Container(
                                id="control-panel", children=generateControls()
                            ),
                        ],
                        lg=3,
                        className="pretty_container",
                    ),
                    dbc.Col(
                        [
                            html.H2(
                                "Visualisation",
                                style={"textAlign": "center", "justify": "center"},
                            ),
                            dbc.Container(
                                id="data-panel", children=preparePanel(fetchData(1))
                            ),
                            html.Div(
                                id="intermediate-valueLive", style={"display": "none"}
                            ),
                            html.Div(
                                id="intermediate-valueButtons",
                                style={"display": "none"},
                            ),
                            html.Div(
                                id="intermediate-valueLast", style={"display": "none"}
                            ),
                            html.Div(id="placeholder", style={"display": "none"}),
                            html.Div(id="intermediate-valueSlider", style={"display": "none"}),
                        ],
                        lg=8,
                        className="pretty_container",
                    ),
                ],
                className="mini_container mt-4, h-100",
            ),
            html.Div([dcc.Graph(id="graph"),
                      dbc.Button(
                          "Clear",
                          color="secondary",
                          id="clear-button",
                          className="mt-1",
                      ),
                      ],
                     className="mini_container"),
        ]
    )

def preparePanel(json):
    return dbc.Container(
        [
            dbc.Row(
                [
                    html.H5(
                        "Patient: "
                        + json.get("firstname")
                        + " "
                        + json.get("lastname")
                        + "   Date: "
                        + str(datetime.fromtimestamp(json.get("timestamp"))).split(".")[0] if json else ""
                    )
                ],
                className="md-4",
                align="center",
                justify="center",
            ),
            updateData(json.get("trace").get("sensors") if json else []),
        ],
        className="h-100, mh-100",
    )
