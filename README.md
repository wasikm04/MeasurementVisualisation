# MeasurementVisualisation

## 1. Project goal
The main goal of the program was to implement web application in Python to graphic
visualisation of data collected by device for monitoring walk habits and patterns of elderly
and disabled persons. The device consists of 6 sensors (3 on each foot) and the main
functionality of the program was graphic visualisation of each sensor, ability to browse
measurement history for last 10 minutes and presenting alerts reported by device.

## 2. Description
Application was created using Dash.plotly which is a Python library to develop reactive web applications. It significantly
simplifies developing graphics user interface in data-related applications associated with
data visualization, data exploration, data analysis, modeling data and reporting.

During browsing of archival measurements, the current ones will still be recorded in
the Cloud Firestore so that they can also be accessed and viewed. We can also switch to the Live
mode at any time.
## 3. Example

![](https://github.com/wasikm04/MeasurementVisualisation/blob/master/img/visualisation.gif)

### Views of application

<img src="https://github.com/wasikm04/MeasurementVisualisation/blob/master/img/feets.png" width="800"/>
<img src="https://github.com/wasikm04/MeasurementVisualisation/blob/master/img/graph.png" width="800"/>