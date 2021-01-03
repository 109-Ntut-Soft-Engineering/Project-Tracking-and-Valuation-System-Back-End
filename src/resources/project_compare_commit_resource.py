from flask_restful import Resource
from models.project_commit_model import ProjectCommitModel
from conn_tool import ConnTool
from common import status_code


class ProjectCompareCommitResource(Resource):
    def __init__(self):
        self._model = ProjectCommitModel(ConnTool())

    def get(self, pid1, pid2):
        commits = self._model.get_compare_project_commit(pid1, pid2)
        return commits, status_code.OK