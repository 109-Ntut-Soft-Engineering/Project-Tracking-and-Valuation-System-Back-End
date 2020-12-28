import firebase_admin
from firebase_admin import credentials, firestore, auth
import os, sys

from src.common import constant

class FakeConnTool():
    def __init__(self):
        # connect cloud firestore
        firebase_key = os.path.abspath(
            os.path.join(__file__, '../../src/testFirebaseKey.json'))
        if not firebase_admin._apps:
            cred = credentials.Certificate(firebase_key)
            firebase_admin.initialize_app(cred)

        # set property
        self._db = firestore.client()
        self._uid = constant.TEST_UID

    @property
    def db(self):
        return self._db

    @property
    def uid(self):
        return self._uid
