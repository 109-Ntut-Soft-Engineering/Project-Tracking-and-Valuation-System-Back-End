from flask import jsonify
from flask_restful import Resource
from models.project_commit_model import ProjectCommitModel
import sys

class ProjectCommitResource(Resource):
    def __init__(self):
        self._model = ProjectCommitModel()

    def get(self, pid):
        print(pid, file=sys.stderr)
        commits = self._model.get_project_commit_info(pid)
        print(commits, file=sys.stderr)
        return commits, 200