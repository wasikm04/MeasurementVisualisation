import requests
import time
URL = "http://tesla.iem.pw.edu.pl:9080/v2/monitor/"

def fetchData(patientId):
    data = requests.get(URL + str(patientId)).json()
    data["timestamp"] = time.time()
    data["id"] = patientId
    return data