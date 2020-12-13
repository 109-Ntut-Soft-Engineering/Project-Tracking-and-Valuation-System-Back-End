from models.project_code_frequency_model import ProjectCodeFrequencyModel
from flask_restful import Resource
from entities.project import Project
from common import status_code


class ProjectCodeFrequencyResource(Resource):
    def __init__(self):
        self._test_token = 'ef4164107b7e4e2505abd8fced70951f44e51964'
        self._model = ProjectCodeFrequencyModel(self._test_token)

    def get(self, name):
        print('name', name)
        return {"code_freq": self._model.get_code_freq(name, self._test_token)}, status_code.OK
