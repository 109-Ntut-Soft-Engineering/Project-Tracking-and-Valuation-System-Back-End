from flask_restful import Resource
from models.project_model import ProjectModel
from conn_tool import ConnTool

class RepositoryResource(Resource):
    def __init__(self):
        self._projectModel = ProjectModel(ConnTool())

    def get(self, pid):

        return self._projectModel.get_avail_repos(pid)
