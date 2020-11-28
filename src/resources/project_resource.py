from flask import jsonify, abort
from flask_restful import Resource, reqparse
from resources.base_resource import BaseResource
from models.project import Project
from common import status_code
from common.status_code import is_client_error
from common.util import is_iter_empty

class ProjectResource(BaseResource):
    def __init__(self):
        super().__init__()

    def get(self, name=None):
        data = self.__project_information(name)
        if is_client_error(data):
            abort(data)
        return jsonify(data)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True, help='name is required.')
        parser.add_argument('owner', required=True, help='owner is required.')
        args = parser.parse_args()

        message = self.__add_project(args['name'], args['owner'])
        if is_client_error(message):
            abort(message)
        return message

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True, help='name is required.')
        args = parser.parse_args()

        message = self.__delete_project(args['name'])
        if is_client_error(message):
            abort(message)
        return message

    def patch(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True, help='name is required.')
        parser.add_argument('owner', required=False)
        parser.add_argument('repositories', required=False)
        args = parser.parse_args()

        message = self.__update_project(args['name'], args['owner'], args['repositories'])
        if is_client_error(message):
            return message
        return message

    def __project_information(self, name=None):
        if name is None:
            projects = self.db.collection(u'projects').where(u'owner', u'array_contains', self.uid).stream()
            return { 'projects': project.to_dict() for project in projects }
        else:
            projects = self.db.collection(u'projects').where(u'name', u'==', name).stream()
            if projects is None:
                return status_code.NOT_FOUND
            return { 'project': project.to_dict() for project in projects }

    def __add_project(self, name, owner):
        if self.__is_project_name_exist(name):
            return status_code.BAD_REQUEST

        pid = self.__next_project_id()
        project = Project(pid=pid, name=name, owner=owner)

        self.db.collection(u'projects').document().set(project.to_dict())

        return status_code.OK

    def __is_project_name_exist(self, name):
        projects = self.db.collection(u'projects').where(u'name', u'==', name).stream()
        return not is_iter_empty(projects)[0]

    def __next_project_id(self):
        projects = self.db.collection(u'projects').stream()
        if projects is None:
            return 1
        *lst, last = projects
        last_project = last.to_dict()
        return int(last.to_dict()['pid']) + 1

    def __delete_project(self, name):
        if not self.__is_project_name_exist(name):
            return status_code.NOT_FOUND

        projects = self.db.collection(u'projects').where(u'name', u'==', name).stream()
        for project in projects:
            project.reference.delete()
        return status_code.OK

    def __update_project(self, name, owner, repositories):
        if not self.__is_project_name_exist(name):
            return status_code.NOT_FOUND

        project = self.__get_unique(self.db.collection(u'projects').where(u'name', u'==', name))
        project_dict = project.to_dict()

        update_data = {}
        if owner != None:
            update_data[u'owner'] = owner
        elif set(owner) & set(project_dict['owner']):
            return status_code.BAD_REQUEST
        if repositories != None:
            update_data[u'repositories'] = repositories
        elif set(repositories) & set(project_dict['repositories']):
            return status_code.BAD_REQUEST
        
        project.set(update_data, merge=True)
        return status_code.OK

    def __get_unique(self, collection):
        return next(collection.stream())