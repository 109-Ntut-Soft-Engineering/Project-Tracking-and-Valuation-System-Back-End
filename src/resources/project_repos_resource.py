from flask import jsonify, abort
from flask_restful import Resource, reqparse
from models.project_model import ProjectModel
from common.status_code import is_client_error
import sys

class ProjectReposResource(Resource):
    def __init__(self):
        self._model = ProjectModel()

    def get(self, pid):
        data, code = self._model.get_project_repos(pid)
        return data, code

    def patch(self, pid):
        parser = reqparse.RequestParser()
        parser.add_argument('collaborator', action='append', required=False)
        parser.add_argument('repositories', type=dict, required=False)
        parser.add_argument('name', required=False)

        args = parser.parse_args()

        if 'repositories' in args:
            repos_parser = reqparse.RequestParser()
            repos_parser.add_argument(
                'Github', action='append', location=('repositories',))
            repos_parser.add_argument(
                'action', required=True,  location=('repositories',))
            args['repositories'] = repos_parser.parse_args(req=args)

        data, code = self._model.update_repos(pid, args)
        return data, code

