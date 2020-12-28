from models.project_code_frequency_model import ProjectCodeFrequencyModel
from flask_restful import Resource
from common import status_code
    

class ProjectCodeFrequencyResource(Resource):
    def __init__(self):
        self._model = ProjectCodeFrequencyModel()

    def get(self, pid):
        try:
            return {"code_freq": self._model.get_code_freq(pid)}, status_code.OK
        except TypeError:
            return {'message': 'cant find pid:{} code frequency'.format(pid)}, 404
