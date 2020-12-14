from conn_tool import ConnTool
from entities.project import Project
from entities.setting import Setting
from common import status_code, error_code
from common.status_code import is_client_error
from common.util import is_iter_empty
import sys
from flask_restful import abort
from google.cloud import firestore
import json
from models.user_model import UserModel
from utilities.github_api_requester import GithubApiRequester
from flask.json import jsonify


class ProjectModel():
    def __init__(self):
        _conn_tool = ConnTool()
        self._db = _conn_tool.db
        self._uid = _conn_tool.uid
        self._userModel = UserModel()

    def get_project_list(self):
        proj_owner = self._db.collection('projects').where(
            'owner', '==', self._uid).get()
        proj_collab = self._db.collection('projects').where(
            'collaborator', 'array_contains', self._uid).get()
        proj_list = []
        self.__build_project_list(proj_list, proj_owner)
        self.__build_project_list(proj_list, proj_collab)
        print(proj_list, file=sys.stderr)
        return {'projects': proj_list}, status_code.OK

    def __build_project_list(self, proj_list, projects):
        for project in projects:
            proj_dic = project.to_dict()
            proj_dic.update({'id': project.id})
            proj_list.append(proj_dic)

    def get_avail_repos(self, pid):
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

    def get_project_repos(self, pid):
        repos = self._db.collection('projects').document(pid).get().to_dict()
        token = UserModel().get_user_githubToken()
        info = {'repos': []}
        if token != None:
            requester = GithubApiRequester(token)
            for repo in requester.get_repoList()['repos']:
                if str(repo['id']) in repos['repositories']['Github']:
                    info['repos'].append(repo)
            return info, status_code.OK
        else:
            None, status_code.NOT_FOUND

    def get_project_setting(self, pid):
        project = self._db.collection('projects').document(pid).get()
        if project.exists:
            proj_dic = project.to_dict()
            setting = Setting(proj_dic['name'], proj_dic['owner'], proj_dic['collaborator'])
            return setting.to_dict(), status_code.OK
        return None, status_code.NOT_FOUND

    def add_project(self, name, owner):
        project = Project(name=name, owner=self._uid)
        self._db.collection('projects').document().set(project.to_dict())
        return None, status_code.OK

    def delete_project(self, pid):
        project = self._db.collection(u'projects').document(pid)
        if not project.get().exists:
            return None, status_code.NOT_FOUND
        project.delete()
        return None, status_code.OK

    def update_repos(self, pid, data):
        project = self._db.collection('projects').document(pid)

        print(data)

        if project.get().exists:
            if data['repositories']['action'] == 'update':
                project.update(
                    {'repositories.Github': firestore.ArrayUnion(data['repositories']['Github']),
                     'updated': firestore.SERVER_TIMESTAMP
                     })
            else:
                project.update(
                    {'repositories.Github': firestore.ArrayRemove(data['repositories']['Github']),
                     'updated': firestore.SERVER_TIMESTAMP
                     })
            return None, status_code.OK
        else:
            return None, status_code.NOT_FOUND

    def update_setting(self, pid, name, collaborator):
        project = self._db.collection('projects').document(pid)

        if project.get().exists:
            project.update({'collaborator': collaborator})
            project.update({'name': name})
            return None, status_code.OK
        else:
            return None, status_code.NOT_FOUND
