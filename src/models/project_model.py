from conn_tool import ConnTool
from entities.project import Project
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

    def get_projects_list(self):
        projects_owner = self._db.collection('projects').where(
            'owner', '==', self._uid).get()
        projects_collab = self._db.collection('projects').where(
            'collaborator', 'array_contains', self._uid).get()
        projList = []
        self.__make_project_list(projList, projects_owner)
        self.__make_project_list(projList, projects_collab)
        return {'projects': projList}

    def __make_project_list(self, projList, projects):
        for project in projects:
            projDic = project.to_dict()
            projDic.update({'id': project.id})
            projList.append(projDic)

    def get_avail_repos(self, pid):
        token = self._userModel.get_user_githubToken()
        if token != None:
            requester = GithubApiRequester(token)
            existRepos = self._db.collection(
                'projects').document(pid).get().to_dict()
            userRepos = requester.get_user_repoList()['repos']
            info = {'repos': []}
            for repo in userRepos:

                if repo['id'] not in existRepos['repositories']['Github']:
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
            for repo in requester.get_user_repoList()['repos']:
                if repo['id'] in repos['repositories']['Github']:
                    info['repos'].append(repo)
            return jsonify(info)
        else:
            status_code.NOT_FOUND

    def get_project_setting(self, pid):
        project = self._db.collection('projects').document(pid).get().to_dict()
        setting = {'setting': {
            'name': None,
            'owner': None,
            'collaborator': []
        }}
        setting['setting']['name'] = project['name']
        setting['setting']['owner'] = project['owner']
        setting['setting']['collaborator'] = project['collaborator']
        return jsonify(setting)

    def add_project(self, name, owner):
        if self.__is_project_name_exist(name):
            return status_code.BAD_REQUEST

        project = Project(name=name, owner=self._uid)

        self._db.collection('projects').document().set(project.to_dict())

        return status_code.OK

    def __is_project_name_exist(self, name):
        projects = self._db.collection(u'projects').where(
            u'name', u'==', name).stream()
        return not is_iter_empty(projects)[0]

    def delete_project(self, pid):
        project = self._db.collection(u'projects').document(pid)
        if not project.get().exists:
            return status_code.NOT_FOUND
        project.delete()
        return status_code.OK

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

        else:
            return status_code.NOT_FOUND

    def update_setting(self, pid, name, collaborator):
        project = self._db.collection('projects').document(pid)

        if project.get().exists:
            project.update({'collaborator': collaborator})
            project.update({'name': name})
        else:
            return status_code.NOT_FOUND
