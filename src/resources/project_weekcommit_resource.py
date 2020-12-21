from flask import jsonify
from flask_restful import Resource
from models.project_weekcommit_model import ProjectWeekCommitModel
from common import status_code
import sys

class ProjectWeekCommitResource(Resource):
    def __init__(self):
        self._model = ProjectWeekCommitModel()

    def get(self, pid):
        try:
            return {"WeekCommit": self._model.get_weekcommit(pid)}, status_code.OK
        except TypeError:
            return {'message': 'cant find pid:{} WeekCommits'.format(pid)}, 404