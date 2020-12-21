from models.Project_issue_message_model import ProjectIssueMessageModel
from flask_restful import Resource
from entities.project import Project
from common import status_code


class ProjectIssueMessageResource(Resource):
    def __init__(self):
        self._model = ProjectIssueMessageModel()

    def get(self, pid):
        try:
            return {"issues": self._model.get_issues(pid)}, status_code.OK
        except TypeError:
            return {'message': 'cant find pid:{} Issues'.format(pid)}, 404