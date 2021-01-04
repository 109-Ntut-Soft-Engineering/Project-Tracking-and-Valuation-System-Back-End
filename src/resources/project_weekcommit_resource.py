from flask import jsonify
from flask_restful import Resource
from models.project_weekcommit_model import ProjectWeekCommitModel
from common import status_code
from conn_tool import ConnTool
import sys

class ProjectWeekCommitResource(Resource):
    def __init__(self):
        self._model = ProjectWeekCommitModel(ConnTool())

    def get(self, pid):
        return {"WeekCommit": self._model.get_weekcommit(pid)}, status_code.OK