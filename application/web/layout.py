import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import requests

URL = "http://tesla.iem.pw.edu.pl:9080/v2/monitor/"


def generateNavbar():
    return dbc.NavbarSimple(brand="Medical Data Visualisation", sticky="top",)


def generateBody():
    return dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.H2("Controller", style={ 'textAlign': 'center', 'justify':"center"} ),
                            dbc.Container(id="control-panel", children=generateControls()),
                        ],
                        lg=4,
                    ),
                    dbc.Col(
                        [
                            html.H2("Visualisation",  style={ 'textAlign': 'center', 'justify':"center"}),
                            dbc.Container(
                                id="data-panel", children=preparePanel(fetchData(1))
                            ),
                        ],
                        lg=8,
                    ),
                ],
                align="start",
                justify="center",
            )
        ],
        className="mt-4, h-100",
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
                                    {"label": "Pacjent 1", "value": 1},
                                    {"label": "Pacjent 2", "value": 2},
                                    {"label": "Pacjent 3", "value": 3},
                                    {"label": "Pacjent 4", "value": 4},
                                    {"label": "Pacjent 5", "value": 5},
                                    {"label": "Pacjent 6", "value": 6},
                                ],
                            )
                        ],
                        lg=6,
                    )
                ],
                className="mt-2",
                justify="center",
            ),
            dbc.Row(
                [
                    dbc.Button("Previous",color="secondary", id="prev-button", className="mr-4"),
                    dbc.Button("Live",color="secondary", id="live-button", className="mr-4"),
                    dbc.Button("Next",color="secondary", id="next-button"),
                ],
                className="mt-2",
                justify="center",
            ),
            dbc.Row(
                [
                    dbc.Button("Previous Anomaly",color="danger", id="prev-anomaly-button", className="mr-2"),
                    dbc.Button("Next Anomaly",color="danger", id="next-anomaly-button" ),
                ],
                className="mt-2",
                justify="center",
            )
        ]
    )


def fetchData(patientId):
    data = requests.get(URL + str(patientId))
    return data.json()


def preparePanel(json):
    return dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(
                        html.H3(
                            "Patient: "
                            + json.get("firstname")
                            + " "
                            + json.get("lastname")
                        ),
                        lg=10,
                    ),
                    # dbc.Col(html.H4("Id: " + str(json.get("id"))),lg=4),
                ],
                className="md-4",
                align="center",
                justify="center",
            ),
            updateData(json.get("trace").get("sensors"))
        ],
        className="h-100, mh-100"
    )


def updateData(sensors):
    return dbc.Container(
            html.Div(
                [
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Input(
                                disabled=True,
                                id="sensor-0",
                                value=sensors[0].get("value"),
                                invalid=sensors[0].get("anomaly") == "true",
                                bs_size="sm",
                            ),
                            width={"size": 2, "order": 4, "offset": 3},
                        ),
                        dbc.Col(
                            dbc.Input(
                                disabled=True,
                                id="sensor-3",
                                value=sensors[3].get("value"),
                                invalid=sensors[3].get("anomaly") == "true",
                                bs_size="sm",
                            ),
                            width={"size": 2, "order": 8, "offset": 2},
                        ),
                    ],
                    className="mt-4",
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
                            ),
                            width={"size": 2, "order": 2, "offset": 2},
                        ),
                        dbc.Col(
                            dbc.Input(
                                disabled=True,
                                id="sensor-4",
                                value=sensors[4].get("value"),
                                invalid=sensors[4].get("anomaly") == "true",
                                bs_size="sm",
                            ),
                            width={"size": 2, "order": 8, "offset": 4},
                        ),
                    ],
                    className="mt-4",
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Input(
                                disabled=True,
                                id="sensor-2",
                                value=sensors[2].get("value"),
                                invalid=sensors[2].get("anomaly") == "true",
                                bs_size="sm",
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
                            ),
                            width={"size": 2, "order": 8, "offset": 2},
                        ),
                    ],
                    className="mt-4"
                ),
                ],
                style={'backgroundImage': 'url(/assets/feets.jpg)', 'backgroundSize': '100% 100%'},
                className="h-100, mh-100, mt-10" 
            ),
            className="h-100, mh-100, mt-10"
    )
