from flask import jsonify, abort
from flask_restful import Resource
from db import Database

class UserResource(Resource):
    def get(self, uid=None):
        db = Database('test_token').db

        if uid is None:
            docs = db.collection(u'users').stream()
            return jsonify({ 'users': doc.to_dict() for doc in docs })
        else:
            docs = db.collection(u'users').where(u'uid', u'==', uid).stream()
            if docs is None:
                abort(404)
            return jsonify({ 'user': doc.to_dict() for doc in docs })