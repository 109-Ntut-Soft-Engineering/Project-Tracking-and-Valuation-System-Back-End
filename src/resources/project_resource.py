from flask import jsonify, abort
from flask_restful import Resource
from db import Database

class ProjectResource(Resource):
    def get(self, pid=None):
        database = Database('test_token')
        db = database.db
        uid = database.uid

        if pid is None:
            docs = db.collection(u'projects').where(u'owner', u'array_contains', uid).stream()
            return jsonify({ 'projects': doc.to_dict() for doc in docs })
        else:
            docs = db.collection(u'projects').where(u'pid', u'==', pid).stream()
            if docs is None:
                abort(404)
            return jsonify({ 'project': doc.to_dict() for doc in docs })