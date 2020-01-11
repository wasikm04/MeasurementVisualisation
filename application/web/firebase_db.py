import time

from firebase_admin import firestore


def save_patient_data(patient_id, data, delete_older_than_10=True):
    database = firestore.client()
    database.collection('patients').add(data)
    if delete_older_than_10: delete_patient_data_older_than_10_min(patient_id)


def save_many_patients_data(datas, delete_older_than_10=True):
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
    return docs_obj


def get_next_data(patient_id, timestamp):
    database = firestore.client()
    docs = database.collection('patients').where(u'id', u'==', patient_id).where(u'timestamp', u'>',
                                                                                 timestamp).order_by(
        u'timestamp', direction=firestore.Query.ASCENDING).limit(1).stream()
    docs_obj = []
    for doc in docs:
        docs_obj.append(doc.to_dict())
    return docs_obj


def get_previous_data(patient_id, timestamp):
    database = firestore.client()
    docs = database.collection('patients').where(u'id', u'==', patient_id).where(u'timestamp', u'<',
                                                                                 timestamp).order_by(
        u'timestamp', direction=firestore.Query.DESCENDING).limit(1).stream()
    docs_obj = []
    for doc in docs:
        docs_obj.append(doc.to_dict())
    return docs_obj


def get_next_anomaly(patient_id, timeout):
    pass


def get_previous_anomaly(patient_id, timeout):
    pass
