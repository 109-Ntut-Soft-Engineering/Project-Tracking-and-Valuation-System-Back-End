from flask import jsonify, abort
from flask_restful import Resource, reqparse
from resources.base_resource import BaseResource
from entities.repo import Repo
from common import status_code, error_code
from common.status_code import is_client_error
from common.util import is_iter_empty
from utilities.git_api_requester import GitApiRequester
from models.user_model import UserModel


class RepositoryResource(BaseResource):
    def __init__(self):
        super().__init__()
        self._userModel = UserModel(self.db, self.uid)

    def get(self, source):
        if source == 'Github':
            return self.__get_github_repos()

    def __get_github_repos(self):
        token = self._userModel.get_user_githubToken()
        if token != None:
            requester = GitApiRequester(token)
            return jsonify(requester.get_repoList())
        else:
            return {
                'message': '尚未連結Github'
            }, status_code.NOT_FOUND
