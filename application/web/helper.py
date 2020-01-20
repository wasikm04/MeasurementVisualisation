import random

import requests
import time
URL = "http://tesla.iem.pw.edu.pl:9080/v2/monitor/"

def fetchData(patientId):
    r = random.randint(0, 5)
    data = requests.get(URL + str(patientId)).json()
    data['trace']['sensors'][r]['anomaly'] = True if (time.time() * 10000) % 100 < 10 else False # TODO: DELETE??????
    print((time.time() * 10000) % 100)
    print(data['trace']['sensors'][r]['anomaly'])
    data["timestamp"] = time.time()
    data["id"] = patientId
    return data