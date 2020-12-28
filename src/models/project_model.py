from conn_tool import ConnTool
from entities.project import Project
from entities.setting import Setting
from common import status_code, error_code

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
        return {'projects': proj_list}, status_code.OK

    def __build_project_list(self, proj_list, projects):
        for project in projects:
            tmpData = project.to_dict()
            tmpData['owner'] = self._userModel.get_user_info_by_uid(
                tmpData['owner'])[0]
            proj_dic = Project.from_dict(tmpData).to_dict()
            proj_dic.update({'id': project.id})
            proj_list.append(proj_dic)

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
        project, token = self._db.collection(
            'projects').document(pid).get().to_dict(), None
        if project['owner'] == self._uid:
            token = UserModel().get_user_githubToken()
        else:
            token = UserModel().get_user_githubToken(project['owner'])
        info = {'repos': []}

        if token != None:
            requester = GithubApiRequester(token)
            for repo in requester.get_user_repoList()['repos']:
                if repo['id'] in project['repositories']['Github']:
                    info['repos'].append(repo)
            return info, status_code.OK
        else:
            None, status_code.NOT_FOUND

    def get_project_setting(self, pid):
        project = self._db.collection('projects').document(pid).get()
        if project.exists:
            proj_dic = project.to_dict()
            setting = Setting(proj_dic['name'], proj_dic['collaborator'])
            return setting.to_dict(), status_code.OK
        return None, status_code.NOT_FOUND

    def add_project(self, name):
        if self.__is_project_name_used(name):
            return None, status_code.BAD_REQUEST

        project = Project(name=name, owner=self._uid,
                          updated=firestore.SERVER_TIMESTAMP)
        project_dict = {
            'name': project.name,
            'owner': project.owner,
            'collaborator': project.collaborator,
            'repositories': project.repositories,
            'updated': project.updated
        }

        self._db.collection('projects').document().set(project_dict)
        return None, status_code.OK

    def __is_project_name_used(self, name):
        projects = self._db.collection('projects').where(
            'name', '==', name).where('owner', '==', self._uid).get()
        for project in projects:
            if project.to_dict()['owner'] == self._uid:
                return True
        return False

    def delete_project(self, pid):
        project = self._db.collection('projects').document(pid)
        if project.get().exists and project.get().to_dict()['owner'] == self._uid:
            project.delete()
            return None, status_code.OK
        return None, status_code.NOT_FOUND

    def update_repos(self, pid, data):
        project = self._db.collection('projects').document(pid)

        print(data)

        if project.get().exists:
            if not self.__is_project_owner(project.get().to_dict(), self._uid):
                return None, status_code.OK

            action = data['repositories']['action']
            if action == 'update':
                project.update(
                    {'repositories.Github': firestore.ArrayUnion(data['repositories']['Github']),
                     'updated': firestore.SERVER_TIMESTAMP
                     })
            elif action == 'remove':
                project.update(
                    {'repositories.Github': firestore.ArrayRemove(data['repositories']['Github']),
                     'updated': firestore.SERVER_TIMESTAMP
                     })
            else:
                return 'missing action', status_code.BAD_REQUEST
            return None, status_code.OK
        else:
            return None, status_code.NOT_FOUND

    def __is_project_owner(self, project, uid):
        return project['owner'] == uid

    def update_collaborator(self, pid, collaborator, action):
        project = self._db.collection('projects').document(pid)

        if project.get().exists:

            if action == 'add':
                info, code = self._userModel.get_user_info_by_email(
                    collaborator)
                if code == status_code.NOT_FOUND:
                    return info, code
                elif info['uid'] in project.get().to_dict()['collaborator']:
                    info, code = {'msg': '協作者已存在！'}, status_code.BAD_REQUEST
                elif info['uid'] == self._uid:
                    info, code = {'msg': '您已是專案擁有者！'}, status_code.BAD_REQUEST
                else:
                    project.update(
                        {'collaborator': firestore.ArrayUnion([info['uid']]),
                         'updated': firestore.SERVER_TIMESTAMP
                         })
                    code = status_code.OK
                return info, code
            elif action == 'remove':
                project.update(
                    {'collaborator': firestore.ArrayRemove([collaborator]),
                     'updated': firestore.SERVER_TIMESTAMP
                     })
                return {'msg': '移除成功！'}, status_code.OK
            else:
                return {'msg': 'miss action'}, status_code.BAD_REQUEST

        else:
            return {'msg': 'Project Not Found'}, status_code.NOT_FOUND

    def update_name(self, pid, name):
        project = self._db.collection('projects').document(pid)
        if project.get().exists:

            if name != '':
                project.update(
                    {'name': name,
                     'updated': firestore.SERVER_TIMESTAMP
                     })
                return None, status_code.OK
            else:
                return 'name is require', status_code.BAD_REQUEST

        else:
            return None, status_code.NOT_FOUND
