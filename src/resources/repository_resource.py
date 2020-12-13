from flask import jsonify, abort
from flask_restful import Resource, reqparse
from entities.repo import Repo
from common import status_code, error_code
from common.status_code import is_client_error
from common.util import is_iter_empty
from conn_tool import ConnTool
from models.user_model import UserModel
from utilities.github_api_requester import GithubApiRequester
from models.project_model import ProjectModel


class RepositoryResource(Resource):
    def __init__(self):
        conn_tool = ConnTool()
        self._db = conn_tool.db
        self._uid = conn_tool.uid
        self._userModel = UserModel()

    def get(self, pid):

        return self.__get_avail_repos(pid)

    def __get_avail_repos(self, pid):
        token = self._userModel.get_user_githubToken()
        if token != None:
            requester = GithubApiRequester(token)
            existRepos = self._db.collection(
                'projects').document(pid).get().to_dict()
            userRepos = requester.get_repoList()['repos']
            info = {'repos': []}
            for repo in userRepos:

                if str(repo['id']) not in existRepos['repositories']['Github']:
                    info['repos'].append(repo)
            return jsonify(info)
        else:
            return {
                'message': '尚未連結Github'
            }, status_code.NOT_FOUND
