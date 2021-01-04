from models.project_weekcommit_model import ProjectWeekCommitModel
from flask_restful import Resource
from conn_tool import ConnTool
from common import status_code


class ProjectCompareWeekCommitResource(Resource):
    def __init__(self):
        self._model = ProjectWeekCommitModel(ConnTool())

    def get(self, pid1, pid2):
        # try:
        #     return {"code_freq": self._model.get_compare_code_frequency(pid1, pid2)}, status_code.OK
        # except TypeError:
        #     return {'message': 'cant find data of pid:{} and pid:{}code frequency'.format(pid1, pid2)}, 404
        return {"week_commit": self._model.get_compare_week_commit(pid1, pid2)}, status_code.OK