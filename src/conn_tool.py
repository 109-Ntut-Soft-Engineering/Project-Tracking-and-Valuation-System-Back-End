import firebase_admin
from firebase_admin import credentials, firestore, auth
import config as config
import sys
import os
from common.util import verify_Idtoken
from flask import request
from flask_restful import abort


class ConnTool:
    def __init__(self):
        # 解決root的問題(之前的兩個可以不用了)
        firebaseKey = os.path.abspath(os.path.join(__file__, '..'))
        if not config.TEST:
            firebaseKey = os.path.join(firebaseKey, 'firebaseKey.json')
        else:
            firebaseKey = os.path.join(firebaseKey, 'testFirebaseKey.json')
        if not firebase_admin._apps:
            cred = credentials.Certificate(firebaseKey)
            firebase_admin.initialize_app(cred)
        self._db = firestore.client()

        if ('Authorization' in request.headers):
            idToken = request.headers['Authorization']
            # print(idToken)
            self._uid = verify_Idtoken(idToken)
        else:
            abort(401)

        # self._uid = '3pCC26BCjFVW5l39bnepCa21gjs1'

    @property
    def db(self):
        if self._db is None:
            sys.exit()
        return self._db

    @property
    def uid(self):
        return self._uid

