import firebase_admin
from firebase_admin import credentials, firestore, auth
import config as config
import sys
import os
from common.util import verify_Idtoken
from flask import request


class Database():
    def __init__(self):
        # 不行的換一個（和專案roots的設定有關
        firebaseKey = os.path.abspath(os.path.join('.', 'src'))
        # firebaseKey = os.path.abspath(os.path.join('.'))
        if not config.TEST:
            firebaseKey = os.path.join(firebaseKey, 'firebaseKey.json')
        else:
            firebaseKey = os.path.join(firebaseKey, 'testFirebaseKey.json')
        if not firebase_admin._apps:
            cred = credentials.Certificate(firebaseKey)
            firebase_admin.initialize_app(cred)
        self._db = firestore.client()
        idToken = request.headers['Authorization']
        print(idToken)
        self._uid = verify_Idtoken(idToken)
        # if idToken == 'test_token':
        #     self._uid = '123'
        # else:
        #     self._uid = verify_Idtiken(idToken)

    @property
    def db(self):
        if self._db is None:
            sys.exit()
        return self._db

    @property
    def uid(self):
        return self._uid
