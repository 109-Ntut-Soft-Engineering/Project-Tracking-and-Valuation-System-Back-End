from models.project_contribution_model import ProjectContributionResource
from flask_restful import Resource
from entities.project import Project
from common import status_code


class ProjectContributionResource(Resource):
    def __init__(self):
        self._test_token = 'ef4164107b7e4e2505abd8fced70951f44e51964'
        self._model = ProjectContributionResource(self._test_token)

    def get(self, name):
        print('name', name)
        return {"contributions": self._model.get_contributions(name, self._test_token)}, status_code.OK
