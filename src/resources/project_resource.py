from flask import jsonify, abort
from flask_restful import reqparse
from resources.base_resource import BaseResource
from entities.project import Project
from models.project_model import ProjectModel
from common import status_code, error_code
from common.status_code import is_client_error
from common.util import is_iter_empty

import sys


class ProjectResource(BaseResource):
    def __init__(self):
        super().__init__()
        self._model = ProjectModel(self.db, self.uid)

    def get(self, name=None):
        data = self._model.get_project_information(name)
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

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True, help='name is required.')
        args = parser.parse_args()

        message = self._model.delete_project(args['name'])
        if is_client_error(message):
            abort(message)
        return message

    def patch(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True, help='name is required.')
        parser.add_argument('owner', action='append', required=False)
        parser.add_argument('repositories', action='append', required=False)
        args = parser.parse_args()

        message = self._model.update_project(args['name'], args['owner'], args['repositories'])
        if is_client_error(message):
            return message
        return message
