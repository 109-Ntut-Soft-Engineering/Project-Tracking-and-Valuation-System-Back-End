from flask import jsonify, abort
from flask_restful import Resource, reqparse
from resources.base_resource import BaseResource
from entities.repo import Repo
from common import status_code, error_code
from common.status_code import is_client_error
from common.util import is_iter_empty

class RepositoryResource(BaseResource):
    def __init__(self):
        super().__init__()

    def get(self, name=None):
        data = self.__repository_information(name)
        if is_client_error(data):
            abort(data)
        return jsonify(data)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True, help='name is required.')
        parser.add_argument('url', required=True, help='url is required.')
        args = parser.parse_args()

        message = self.__add_repository(args['name'], args['url'])
        if is_client_error(message):
            abort(message)
        return message

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True, help='name is required.')
        args = parser.parse_args()

        message = self.__delete_repository(args['name'])
        if is_client_error(message):
            abort(message)
        return message

    def __repository_information(self, name=None):
        if name is None:
            repos = self.db.collection(u'repositories').stream()
            return { 'repositorys': repo.to_dict() for repo in repos }
        else:
            repos = self.db.collection(u'repositories').where(u'name', u'==', name).stream()
            if repos is None:
                return status_code.NOT_FOUND
            return { 'repository': repo.to_dict() for repo in repos }
    
    def __add_repository(self, name, url):
        if self.__is_repository_name_exist(name):
            return status_code.BAD_REQUEST

        rid = self.__next_repository_id()
        repo = Repo(rid=rid, name=name, url=url)

        self.db.collection(u'repositories').document().set(repo.to_dict())

        return status_code.OK

    def __is_repository_name_exist(self, name):
        repos = self.db.collection(u'repositories').where(u'name', u'==', name).stream()
        return not is_iter_empty(repos)[0]
    
    def __next_repository_id(self):
        repos = self.db.collection(u'repositories').stream()
        if repos is None:
            return 1

        idx = 1
        for repo in repos:
            cur_rid = repo.to_dict()['rid']
            if(idx < cur_rid):
                idx = cur_rid
            print(cur_rid)
                
        return idx + 1

    def __delete_repository(self, name):
        if not self.__is_repository_name_exist(name):
            return status_code.NOT_FOUND

        repos = self.db.collection(u'repositories').where(u'name', u'==', name).stream()
        for repo in repos:
            repo.reference.delete()
        return status_code.OK