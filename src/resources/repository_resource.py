from flask_restful import Resource
from models.project_model import ProjectModel


class RepositoryResource(Resource):
    def __init__(self):
        self._projectModel = ProjectModel()

    def get(self, pid):

        return self._projectModel.get_avail_repos(pid)
