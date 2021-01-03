from models.project_code_frequency_model import ProjectCodeFrequencyModel
from flask_restful import Resource
from common import status_code
from conn_tool import ConnTool


class ProjectCompareCodeFrequencyResource(Resource):
    def __init__(self):
        self._model = ProjectCodeFrequencyModel()

    def get(self, pid1, pid2):
        return {"code_freq": self._model.get_compare_code_frequency(pid1, pid2)}, status_code.OK
