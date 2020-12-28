from flask import jsonify, abort
from flask_restful import Resource, reqparse
from models.project_model import ProjectModel


class ProjectsResource(Resource):
    def __init__(self):
        self._model = ProjectModel()

    def get(self):
        data, code = self._model.get_project_list()
        return data, code

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True, help='name is required.')
        args = parser.parse_args()

        data, code = self._model.add_project(args['name'])
        return data, code
