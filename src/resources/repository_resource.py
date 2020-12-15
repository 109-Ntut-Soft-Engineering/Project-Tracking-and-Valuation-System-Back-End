from flask import jsonify, abort
from flask_restful import Resource, reqparse
from entities.repo import Repo
from common import status_code, error_code
from common.status_code import is_client_error
from common.util import is_iter_empty
from models.user_model import UserModel
from utilities.github_api_requester import GithubApiRequester
from models.project_model import ProjectModel


class RepositoryResource(Resource):
    def __init__(self):
        self._projectModel = ProjectModel()

    def get(self, pid):

        return self._projectModel.get_avail_repos(pid)
