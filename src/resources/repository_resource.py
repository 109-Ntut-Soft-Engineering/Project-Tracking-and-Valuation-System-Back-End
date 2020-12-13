from flask import jsonify, abort
from flask_restful import Resource, reqparse
from entities.repo import Repo
from common import status_code, error_code
from common.status_code import is_client_error
from common.util import is_iter_empty
from conn_tool import ConnTool
from models.user_model import UserModel
from utilities.github_api_requester import GithubApiRequester


class RepositoryResource(Resource):
    def __init__(self):
        conn_tool = ConnTool()
        self._db = conn_tool.db
        self._uid = conn_tool.uid
        self._userModel = UserModel()

    def get(self, source):
        if source == 'Github':
            return self.__get_github_repos()

    def __get_github_repos(self):
        token = self._userModel.get_user_githubToken()
        if token != None:
            requester = GithubApiRequester(token)
            return jsonify(requester.get_repoList())
        else:
            return {
                'message': '尚未連結Github'
            }, status_code.NOT_FOUND
