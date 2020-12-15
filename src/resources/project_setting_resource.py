from flask import jsonify, abort
from flask_restful import Resource, reqparse
from models.project_model import ProjectModel
from common.status_code import is_client_error

import sys


class ProjectSettingResource(Resource):
    def __init__(self):
        self._model = ProjectModel()

    def get(self, pid):
        data, code = self._model.get_project_setting(pid)
        return data, code

    def delete(self, pid):
        data, code = self._model.delete_project(pid)
        return data, code

    def patch(self, pid):
        parser = reqparse.RequestParser()
        parser.add_argument('collaborator', action='append', required=False)
        parser.add_argument('name', action='append', required=False)

        args = parser.parse_args()

        data, code = self._model.update_setting(
            pid, args['name'], args['collaborator'])
        return data, code
