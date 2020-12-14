from flask import jsonify, abort
from flask_restful import Resource, reqparse
from models.project_model import ProjectModel
from common.status_code import is_client_error
import sys

class ProjectReposResource(Resource):
    def __init__(self):
        self._model = ProjectModel()

    def get(self, pid):
        return self._model.get_project_repos(pid)

    def patch(self, pid):
        repos_parser = reqparse.RequestParser()
        repos_parser.add_argument(
            'Github', action='append', location=('repositories',))
        repos_args = repos_parser.parse_args()
        message = self._model.update_project(
            pid, repos_args['Github'])
        if is_client_error(message):
            return message
        return message
