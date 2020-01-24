import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

input_style = {
    "backgroundColor": "transparent",
    "borderRadius": "2rem",
    "textAlign": "center",
}


def updateData(sensors):
    return dbc.Container(
        html.Div(
            [
                dbc.Row(className="mt-4", ),
                dbc.Row(className="mt-4", ),
                dbc.Row(className="mt-4", ),
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Input(
                                disabled=True,
                                id="sensor-0",
                                value=sensors[0].get("value") if len(sensors) > 0 else '',
                                invalid=sensors[0].get("anomaly") if len(sensors) > 0 else False,
                                bs_size="sm",
                                style=input_style,
                            ),
                            width={"size": 2, "order": 4, "offset": 2},
                        ),
                        dbc.Col(
                            dbc.Input(
                                disabled=True,
                                id="sensor-3",
                                value=sensors[3].get("value") if len(sensors) > 3 else '',
                                invalid=sensors[3].get("anomaly") if len(sensors) > 3 else False,
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
                                value=sensors[1].get("value") if len(sensors) > 1 else '',
                                invalid=sensors[1].get("anomaly") if len(sensors) > 1 else False,
                                bs_size="sm",
                                style=input_style,
                            ),
                            width={"size": 2, "order": 1, "offset": 1},
                        ),
                        dbc.Col(
                            dbc.Input(
                                disabled=True,
                                id="sensor-4",
                                value=sensors[4].get("value") if len(sensors) > 4 else '',
                                invalid=sensors[4].get("anomaly") if len(sensors) > 4 else False,
                                bs_size="sm",
                                style=input_style,
                            ),
                            width={"size": 2, "order": 10, "offset": 6},
                        ),
                    ],
                ),
                dbc.Row(className="mt-5", ),
                dbc.Row(className="mt-5", ),
                dbc.Row(className="mt-5", ),
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Input(
                                disabled=True,
                                id="sensor-2",
                                value=sensors[2].get("value") if len(sensors) > 2 else '',
                                invalid=sensors[2].get("anomaly") if len(sensors) > 2 else False,
                                bs_size="sm",
                                style=input_style,
                            ),
                            width={"size": 2, "order": 4, "offset": 3},
                        ),
                        dbc.Col(
                            dbc.Input(
                                disabled=True,
                                id="sensor-5",
                                value=sensors[5].get("value") if len(sensors) > 5 else '',
                                invalid=sensors[5].get("anomaly") if len(sensors) > 5 else False,
                                bs_size="sm",
                                style=input_style,
                            ),
                            width={"size": 2, "order": 8, "offset": 2},
                        ),
                    ],
                    className="mb-4",
                ),
                dbc.Row(className="mt-1", ),
            ],
            style={
                "backgroundImage": "url(/assets/feets3.jpg)",
                "backgroundSize": "100% 100%",
            },
            className="h-100, mh-100, mt-10",
        ),
        className="h-100, mh-100, mt-10",
    )
