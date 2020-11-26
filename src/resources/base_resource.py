from flask_restful import Resource
from db import Database

class BaseResource(Resource):
    def __init__(self):
        super().__init__()
        database = Database('test_token')
        self._db = database.db
        self._uid = database.uid

    @property
    def db(self):
        return self._db

    @property
    def uid(self):
        return self._uid