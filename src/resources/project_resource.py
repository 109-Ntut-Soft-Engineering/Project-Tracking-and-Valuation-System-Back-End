from flask import jsonify, abort
from flask_restful import Resource, reqparse
from resources.base_resource import BaseResource
from models.project import Project
from common import error_code
from common.util import is_iter_empty

class ProjectResource(BaseResource):
    def __init__(self):
        super().__init__()

    def get(self, name=None):
        data = self.__project_information(name)
        if data == error_code.NO_SUCH_ELEMENT:
            abort(404)
        return jsonify(data)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True, help="account is required.")
        parser.add_argument('owner', required=True, help="account is required.")
        args = parser.parse_args()

        message = self.__add_project(args['name'], args['owner'])
        return message

    def delete(self, pid):


    def __project_information(self, name=None):
        if name is None:
            projects = self.db.collection(u'projects').where(u'owner', u'array_contains', self.uid).stream()
            return { 'projects': project.to_dict() for project in projects }
        else:
            projects = self.db.collection(u'projects').where(u'name', u'==', name).stream()
            if projects is None:
                return error_code.NO_SUCH_ELEMENT
            return { 'project': project.to_dict() for project in projects }

    def __add_project(self, name, owner):
        if self.__is_project_name_exist(name):
            return error_code.ELEMENT_EXIST

        pid = self.__next_project_id()
        project = Project(pid=pid, name=name, owner=owner)

        self.db.collection(u'projects').document().set(project.to_dict())

        return 200

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

    