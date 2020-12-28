from flask import jsonify
from flask_restful import Resource
from models.project_commit_model import ProjectCommitModel
from conn_tool import ConnTool
import sys
from common import status_code

class ProjectCommitResource(Resource):
    def __init__(self):
        self._model = ProjectCommitModel(ConnTool())

    def get(self, pid):
        commits = self._model.get_project_commit(pid)
        return commits, status_code.OK