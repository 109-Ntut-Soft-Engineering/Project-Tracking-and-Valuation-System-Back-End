from flask import jsonify
from flask_restful import Resource
from resources.base_resource import BaseResource
from models.project_commit_model import ProjectCommitModel
import sys

class ProjectCommitResource(BaseResource):
    def __init__(self):
        super().__init__()
        self._model = ProjectCommitModel(self.db, self.uid)

    def get(self, name):
        print('name = ' + name, file=sys.stderr)
        commits = self._model.get_project_commit_info(name)
        return jsonify(commits)