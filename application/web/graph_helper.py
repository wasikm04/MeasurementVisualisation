from datetime import datetime


def composeGraph(dataList):
    layout_graph = layout
    xList, yList = produceData(dataList)
    data = prepareGraphData(xList, yList)

    if xList: layout_graph["xaxis"] = dict(range=[min(xList), max(xList)])
    if yList: layout_graph["yaxis"] = dict(range=[min(min(yList)) - 30, max(max(yList)) + 30])
    return {'data': data, 'layout': layout_graph}


def produceData(dataList):
    xList = []
    tmp = dict([(0, []), (1, []), (2, []), (3, []), (4, []), (5, [])])
    for obj in dataList:
        xList.append(str(datetime.fromtimestamp(obj.get("timestamp"))).split(" ")[1].split(".")[0])
        data = obj.get("trace").get("sensors")
        for val in data:
            tmp[val.get("id")].append(val.get("value"))

    return xList, [tmp[0], tmp[1], tmp[2], tmp[3], tmp[4], tmp[5]]


def prepareGraphData(xList, yList):
    data = []

    for x in range(6):
        line = dict(
            type="scatter",
            mode="lines+markers",
            name="Sensor " + str(x) + ( "(Left)" if x < 3 else "(Right)"),
            x=xList,
            y=yList[x],
            line=dict(shape="spline", color=colors[x]),
            marker=dict(symbol="diamond")  # , line={"color": colors[x]})
        )
        data.append(line)
    return data


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
