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

    def get_projects_list(self):
        projects = self._db.collection('projects').where(
            'owner', '==', self._uid).get()
        projList = []
        for project in projects:
            projDic = project.to_dict()
            projDic.update({'id': project.id})
            projList.append(projDic)

        return {'projects': projList}

    def get_project_repos(self, pid):
        repos = self._db.collection('projects').document(pid).get().to_dict()
        token = UserModel().get_user_githubToken()
        info = {'repos': []}
        if token != None:
            requester = GithubApiRequester(token)
            for repo in requester.get_repoList()['repos']:
                if str(repo['id']) in repos['repositories']['Github']:
                    info['repos'].append(repo)
            return jsonify(info)
        else:
            status_code.NOT_FOUND

    def add_project(self, name, owner):
        if self.__is_project_name_exist(name):
            return status_code.BAD_REQUEST

        project = Project(name=name, owner=self._uid)

        self._db.collection('projects').document().set(project.to_dict())

        return status_code.OK

    def __is_project_name_exist(self, name):
        projects = self.db.collection(u'projects').where(
            u'name', u'==', name).stream()
        return not is_iter_empty(projects)[0]

    def delete_project(self, name):
        if not self.__is_project_name_exist(name):
            return status_code.NOT_FOUND

        projects = self._db.collection(u'projects').where(
            u'name', u'==', name).stream()
        for project in projects:
            project.reference.delete()
        return status_code.OK

    def update_project(self, pid, data):
        project = self._db.collection('projects').document(pid)

        print(data)

        if project.get().exists:

            if 'repositories' in data:
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
                newData = {}
                if 'name' in data:
                    newData['name'] = data['name']
                if 'collaborator' in data:
                    newData['collaborator'] = data['collaborator']
                project.update(newData)

        else:
            return status_code.NOT_FOUND
        # if not self.__is_project_name_exist(name):
        #     return status_code.NOT_FOUND

        # project = self.__get_unique(self._db.collection(
        #     u'projects').where(u'name', u'==', name))
        # project_dict = self.__init_project(project)

        # update_data = {}
        # code = self.__set_update_data(
        #     project_dict, owner, update_data, 'owner')
        # if is_client_error(code):
        #     return code
        # code = self.__set_update_data(
        #     project_dict, repositories, update_data, 'repositories')
        # if is_client_error(code):
        #     return code

        # if len(update_data) == 0:
        #     return status_code.BAD_REQUEST

        # project.reference.set(update_data, merge=True)
        # return status_code.OK

    def __init_project(self, project):
        project_dict = project.to_dict()
        if project_dict['owner'] is None:
            project_dict['owner'] = []
        if project_dict['repositories'] is None:
            project_dict['repositories'] = []
        return project_dict

    def __set_update_data(self, origin, update, update_data, field_name):
        code = self.__validate_update_array(origin, update, field_name)
        if code == status_code.OK:
            update_data[field_name] = list(
                set(update) | set(origin[field_name]))
        elif is_client_error(code):
            return code
        return status_code.OK

    def __validate_update_array(self, origin, update, field_name):
        if update is None:
            return error_code.NO_SUCH_ELEMENT
        if len(set(origin) & set(update)) == 0:
            return status_code.OK
        else:
            return status_code.BAD_REQUEST

    def __get_unique(self, collection):
        return next(collection.stream())
