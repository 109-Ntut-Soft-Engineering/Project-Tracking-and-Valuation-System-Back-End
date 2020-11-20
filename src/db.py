import firebase_admin
from firebase_admin import credentials, firestore
import config as config
import sys

class Database():
    def __init__(self):
        firebaseKey = './software-engineer-back-end/src/'
        if not config.TEST:
            firebaseKey += 'firebaseKey.json'
        else:
            firebaseKey += 'testFirebaseKey.json'
        cred = credentials.Certificate(firebaseKey)
        firebase_admin.initialize_app(cred)
        self._db = firestore.client()

    @property
    def db(self):
        if self._db is None:
            sys.exit()
        return self._db