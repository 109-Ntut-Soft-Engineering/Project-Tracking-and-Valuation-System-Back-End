from models.Project_issue_message_model import ProjectIssueMessageModel
from flask_restful import Resource
from entities.project import Project
from common import status_code


class ProjectIssueMessageResource(Resource):
    def __init__(self):
        self._test_token = 'test_token'
        self._model = ProjectIssueMessageModel(self._test_token)

    def get(self, name):
        print('name', name)
        return {"issue": self._model.get_issues(name, self._test_token)}, status_code.OK