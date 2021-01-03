from flask import jsonify, abort
from flask_restful import Resource, reqparse
from models.project_model import ProjectModel
from conn_tool import ConnTool

import sys


class ProjectSettingResource(Resource):
    def __init__(self):
        self._model = ProjectModel(ConnTool())

    def get(self, pid):
        data, code = self._model.get_project_setting(pid)
        return data, code

    def delete(self, pid):
        data, code = self._model.delete_project(pid)
        return data, code

    def patch(self, pid):
        parser = reqparse.RequestParser()
        parser.add_argument('collaborator', required=False)
        parser.add_argument('collabAction',  required=False)

        parser.add_argument('name',  required=False)

        args = parser.parse_args()
        data, code = 'wrong args', 404
        print(args)
        if args['collaborator'] != None and args['collabAction'] != None:
            data, code = self._model.update_collaborator(
                pid, args['collaborator'], args['collabAction'])
        elif args['name'] != None:
            data, code = self._model.update_name(
                pid, args['name'])

        return data, code
