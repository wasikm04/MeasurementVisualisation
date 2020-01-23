import time

from firebase_admin import firestore


def save_patient_data(data, delete_older_than_10=True):
    database = firestore.client()
    database.collection('patients').add(data)
    if delete_older_than_10: delete_patient_data_older_than_10_min(data['id'])


def save_many_patients_data(datas, delete_older_than_10=False):
    database = firestore.client()
    for data in datas:
        database.collection('patients').add(data)
    if delete_older_than_10:
        for data in datas:
            delete_patient_data_older_than_10_min(data['id'])


def get_all_documents():
    database = firestore.client()
    docs = database.collection('patients').stream()
    docs_obj = []
    for doc in docs:
        docs_obj.append(doc.to_dict())
    return docs_obj


def get_all_patient_documents(patient_id):
    database = firestore.client()
    docs = database.collection('patients').where(u'id', u'==', patient_id).stream()
    docs_obj = []
    for doc in docs:
        docs_obj.append(doc.to_dict())
    return docs_obj


def delete_patient_data_older_than_10_min(patient_id):
    database = firestore.client()
    curr_time = time.time()
    ten_min_ago = curr_time - 600
    docs = database.collection('patients').where(u'id', u'==', patient_id).where(u'timestamp', u'<',
                                                                                 ten_min_ago).stream()
    for doc in docs:
        database.collection('patients').document(doc.id).delete()


def delete_all_patients_data_older_than_10_min():
    database = firestore.client()
    curr_time = time.time()
    ten_min_ago = curr_time - 600
    docs = database.collection('patients').where(u'timestamp', u'<', ten_min_ago).stream()
    for doc in docs:
        database.collection('patients').document(doc.id).delete()


def get_last_patient_document(patient_id):
    database = firestore.client()
    docs = database.collection('patients').where(u'id', u'==', patient_id).order_by(u'timestamp').limit(1).stream()
    docs_obj = []
    for doc in docs:
        docs_obj.append(doc.to_dict())
    return docs_obj[0]


def get_next_data(patient_id, timestamp):
    database = firestore.client()
    docs = database \
        .collection('patients') \
        .where(u'id', u'==', patient_id) \
        .where(u'timestamp', u'>', timestamp) \
        .order_by(u'timestamp', direction=firestore.Query.ASCENDING) \
        .limit(1) \
        .stream()
    docs_obj = []
    for doc in docs:
        docs_obj.append(doc.to_dict())
    return docs_obj


def get_previous_data(patient_id, timestamp):
    database = firestore.client()
    docs = database \
        .collection('patients') \
        .where(u'id', u'==', patient_id) \
        .where(u'timestamp', u'<', timestamp) \
        .order_by(u'timestamp', direction=firestore.Query.DESCENDING) \
        .limit(1) \
        .stream()
    docs_obj = []
    for doc in docs:
        docs_obj.append(doc.to_dict())
    return docs_obj


def get_all_patients_data(patient_id):
    database = firestore.client()
    docs = database \
        .collection('patients') \
        .where(u'id', u'==', patient_id) \
        .stream()
    docs_obj = []
    for doc in docs:
        docs_obj.append(doc.to_dict())
    return docs_obj


def check_anomaly_in_patients_data(patient_data):
    for sensor in patient_data['trace']['sensors']:
        if sensor['anomaly']:
            return True
    return False


def get_next_anomaly(patient_id, timestamp):
    patients_data = get_all_patients_data(patient_id)
    patients_next_anomalies = []

    for p in patients_data:
        if p['timestamp'] > timestamp and check_anomaly_in_patients_data(p):
            patients_next_anomalies.append(p)

    patients_next_anomalies = sorted(patients_next_anomalies, key=lambda k: k['timestamp'])
    #print(len(patients_next_anomalies))
    #print(patients_next_anomalies[0] if patients_next_anomalies and len(patients_next_anomalies) > 0 else [])
    return patients_next_anomalies[0] if patients_next_anomalies and len(patients_next_anomalies) > 0 else []


def get_previous_anomaly(patient_id, timestamp):
    patients_data = get_all_patients_data(patient_id)
    patients_prev_anomalies = []

    for p in patients_data:
        if p['timestamp'] < timestamp and check_anomaly_in_patients_data(p):
            patients_prev_anomalies.append(p)

    patients_prev_anomalies = sorted(patients_prev_anomalies, key=lambda k: k['timestamp'], reverse=True)
    #print(len(patients_prev_anomalies))
    #print(patients_prev_anomalies[0] if patients_prev_anomalies and len(patients_prev_anomalies) > 0 else [])
    return patients_prev_anomalies[0] if patients_prev_anomalies and len(patients_prev_anomalies) > 0 else []
