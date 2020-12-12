from flask import jsonify, abort
from flask_restful import Resource, reqparse
from models.project_model import ProjectModel
from common.status_code import is_client_error

class ProjectsResource(Resource):
    def __init__(self):
        self._model = ProjectModel('test_token')

    def get(self):
        data = self._model.get_projects_information()
        if is_client_error(data):
            abort(data)
        return jsonify(data)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True, help='name is required.')
        parser.add_argument('owner', action='append', required=True, help='owner is required.')
        args = parser.parse_args()

        message = self._model.add_project(args['name'], args['owner'])
        if is_client_error(message):
            abort(message)
        return message