import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from datetime import datetime
import time
from helper import *
from firebase_db import save_patient_data



input_style = {
    "backgroundColor": "transparent",
    "borderRadius": "2rem",
    "textAlign": "center",
}


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
                        className="pretty_container"
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
                        ],
                        lg=8, 
                        className="pretty_container"
                    ),
                ],
                className="mini_container mt-4, h-100",
            ),
            html.Div(
                [dcc.Graph(id="graph")], className="mini_container"
            )
        ]
    )


def generateControls():
    return dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.Select(
                                id="patient-select",
                                value=1,
                                options=[
                                    {"label": "Patient 1", "value": 1},
                                    {"label": "Patient 2", "value": 2},
                                    {"label": "Patient 3", "value": 3},
                                    {"label": "Patient 4", "value": 4},
                                    {"label": "Patient 5", "value": 5},
                                    {"label": "Patient 6", "value": 6},
                                ],
                            )
                        ],
                        lg=10,
                    )
                ],
                className="mt-2",
                justify="center",
            ),
            dbc.Row(
                [
                    dbc.Button(
                        "Previous",
                        color="secondary",
                        id="prev-button",
                        className="mr-4",
                    ),
                    dbc.Button("Next", color="secondary", id="next-button"),
                ],
                className="mt-2",
                justify="center",
            ),
            dbc.Row(
                [
                    dbc.Button(
                        "Stop", color="secondary", id="stop-button", className="mr-4"
                    ),
                    dbc.Button("Live", color="secondary", id="live-button"),
                ],
                className="mt-2",
                justify="center",
            ),
            dbc.Row(
                [
                    dbc.Button(
                        "Previous Anomaly",
                        color="danger",
                        id="prev-anomaly-button",
                        className="mb-2",
                    ),
                    dbc.Button(
                        "Next Anomaly", color="danger", id="next-anomaly-button"
                    ),
                ],
                className="mt-2",
                justify="center",
            ),
            dbc.Row(
                [html.H5("Live update of patients data.", id="current-action")],
                className="mt-2",
                justify="center",
            ),
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
                            + str(datetime.fromtimestamp(json.get("timestamp"))).split(".")[0]
                        )
                ],
                className="md-4",
                align="center",
                justify="center",
            ),
            updateData(json.get("trace").get("sensors")),
        ],
        className="h-100, mh-100",
    )


def updateData(sensors):
    return dbc.Container(
        html.Div(
            [
                dbc.Row(className="mt-4",),
                dbc.Row(className="mt-4",),
                dbc.Row(className="mt-4",),
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Input(
                                disabled=True,
                                id="sensor-0",
                                value=sensors[0].get("value"),
                                invalid=sensors[0].get("anomaly") == "true",
                                bs_size="sm",
                                style=input_style,
                            ),
                            width={"size": 2, "order": 4, "offset": 2},
                        ),
                        dbc.Col(
                            dbc.Input(
                                disabled=True,
                                id="sensor-3",
                                value=sensors[3].get("value"),
                                invalid=sensors[3].get("anomaly") == "true",
                                bs_size="sm",
                                style=input_style,
                            ),
                            width={"size": 2, "order": 8, "offset": 3},
                        ),
                    ],
                    className="ml-5 mt-5",
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Input(
                                disabled=True,
                                id="sensor-1",
                                value=sensors[1].get("value"),
                                invalid=sensors[4].get("anomaly") == "true",
                                bs_size="sm",
                                style=input_style,
                            ),
                            width={"size": 2, "order": 1, "offset": 1},
                        ),
                        dbc.Col(
                            dbc.Input(
                                disabled=True,
                                id="sensor-4",
                                value=sensors[4].get("value"),
                                invalid=sensors[4].get("anomaly") == "true",
                                bs_size="sm",
                                style=input_style,
                            ),
                            width={"size": 2, "order": 10, "offset": 6},
                        ),
                    ],
                ),
                dbc.Row(className="mt-5",),
                dbc.Row(className="mt-5",),
                dbc.Row(className="mt-5",),
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Input(
                                disabled=True,
                                id="sensor-2",
                                value=sensors[2].get("value"),
                                invalid=sensors[2].get("anomaly") == "true",
                                bs_size="sm",
                                style=input_style,
                            ),
                            width={"size": 2, "order": 4, "offset": 3},
                        ),
                        dbc.Col(
                            dbc.Input(
                                disabled=True,
                                id="sensor-5",
                                value=sensors[5].get("value"),
                                invalid=sensors[5].get("anomaly") == "true",
                                bs_size="sm",
                                style=input_style,
                            ),
                            width={"size": 2, "order": 8, "offset": 2},
                        ),
                    ],
                    className="mb-4",
                ),
                dbc.Row(className="mt-1",),
            ],
            style={
                "backgroundImage": "url(/assets/feets3.jpg)",
                "backgroundSize": "100% 100%",
            },
            className="h-100, mh-100, mt-10",
        ),
        className="h-100, mh-100, mt-10",
    )

