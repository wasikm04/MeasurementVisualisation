import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc


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
                    html.Div(
                        dbc.Button(
                            "Previous",
                            color="secondary",
                            id="prev-button",
                            className="mr-4, btn-block",
                        ),
                        className="btn-container-left"
                    ),
                    html.Div(
                        dbc.Button(
                            "Next",
                            color="secondary",
                            id="next-button",
                            className="btn-block"
                        ),
                        className="btn-container-right"
                    )
                ],
                className="mt-2",
                justify="center"
            ),
            dbc.Row(
                [
                    html.Div(
                        dbc.Button(
                            "Stop",
                            color="secondary",
                            id="stop-button",
                            className="btn-block"
                        ),
                        className="btn-container-left"
                    ),
                    html.Div(
                        dbc.Button(
                            "Live",
                            color="secondary",
                            id="live-button",
                            className="btn-block"
                        ),
                        className="btn-container-right"
                    ),
                ],
                className="mt-2",
                justify="center"
            ),
            dbc.Row(
                [
                    html.Div(
                        dbc.Button(
                            "Previous Anomaly",
                            color="danger",
                            id="prev-anomaly-button",
                            className="btn-block"
                        ),
                        className="anomaly-button"
                    ),
                    html.Div(
                        dbc.Button(
                            "Next Anomaly",
                            color="danger",
                            id="next-anomaly-button",
                            className="btn-block"
                        ),
                        className="anomaly-button"
                    ),
                ],
                className="mt-2",
                justify="center",
            ),
            dbc.Row(
                [html.H6("Live update of patients data.", id="current-action")],
                className="mt-2",
                justify="center",
            ),
            html.Div(
                [dcc.Slider(id="timestamp-slider", min=0, max=10, step=0.1, value=10,
                            marks={
                                0: {'label': '-10 min', 'style': {'color': '#77b0b1'}},
                                10: {'label': 'Live', 'style': {'color': '#f50'}}
                            })],
                className="mt-4",
            ),
            dbc.Row(
                [html.H6("", id="text-slider")],
                className="mt-4",
                justify="center",
            ),
        ]
    )
