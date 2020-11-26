from flask import jsonify, abort
from flask_restful import Resource
from common import error_code
from models.project_and_repository_model import ProjectAndRepositoryModel

class ProjectResource(Resource):
    def get(self, pid=None):
        data = ProjectAndRepositoryModel.project_information(pid)
        if data == error_code.NO_SUCH_ELEMENT:
            abort(404)
        return jsonify(data)