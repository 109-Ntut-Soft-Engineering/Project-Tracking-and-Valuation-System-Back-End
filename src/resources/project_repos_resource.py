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
        parser = reqparse.RequestParser()
        parser.add_argument('repositories', type=dict, required=True)

        args = parser.parse_args()

        if 'repositories' in args:
            repos_parser = reqparse.RequestParser()
            repos_parser.add_argument(
                'Github', action='append', type=int, location=('repositories',))
            repos_parser.add_argument(
                'action', required=True,  location=('repositories',))
            args['repositories'] = repos_parser.parse_args(req=args)

        message = self._model.update_repos(pid, args)
        if is_client_error(message):
            return message
        return message
