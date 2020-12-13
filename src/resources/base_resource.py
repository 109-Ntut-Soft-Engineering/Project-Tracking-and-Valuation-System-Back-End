from flask_restful import Resource, abort
from db import Database


class BaseResource(Resource):
    # method_decorators = [authenticate]
    # @authenticate
    def __init__(self):
        super().__init__()
        database = Database()
        self._db = database.db
        self._uid = database.uid
        print(self._uid)


    @property
    def db(self):
        return self._db

    @property
    def uid(self):
        return self._uid
