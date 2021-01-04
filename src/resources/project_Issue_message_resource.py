from models.Project_issue_message_model import ProjectIssueMessageModel
from flask_restful import Resource
from entities.project import Project
from conn_tool import ConnTool
from common import status_code


class ProjectIssueMessageResource(Resource):
    def __init__(self):
        self._model = ProjectIssueMessageModel(ConnTool())

    def get(self, pid):
        return {"issues": self._model.get_issues(pid)}, status_code.OK
    