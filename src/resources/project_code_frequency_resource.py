from models.project_code_frequency_model import ProjectCodeFrequencyModel
from flask_restful import Resource
from common import status_code
from conn_tool import ConnTool


class ProjectCodeFrequencyResource(Resource):
    def __init__(self):
        self._model = ProjectCodeFrequencyModel(ConnTool())

    def get(self, pid):
        return {"code_freq": self._model.get_code_freq(pid)}, status_code.OK

