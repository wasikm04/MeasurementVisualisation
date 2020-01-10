import time

from firebase_admin import firestore


def save_patient_data(patient_id, data):
    database = firestore.client()
    database.collection('patients').add(data)
    delete_patient_data_older_than_10_min(patient_id)


def get_all_patient_data(patient_id):
    database = firestore.client()
    return database.collection('patients')


def delete_patient_data_older_than_10_min(patient_id):
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
    return docs_obj

