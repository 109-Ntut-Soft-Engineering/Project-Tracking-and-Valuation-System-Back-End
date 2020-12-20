from flask import jsonify
from flask_restful import Resource
from models.project_weekcommit_model import ProjectWeekCommitModel
from common import status_code
import sys

class ProjectWeekCommitResource(Resource):
    def __init__(self):
        self._test_token = 'test_token'
        self._model = ProjectWeekCommitModel(self._test_token)

    def get(self, name):
        return {"WeekCommit": self._model.get_weekcommit(name, self._test_token)}, status_code.OK