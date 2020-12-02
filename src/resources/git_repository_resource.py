from utilities.git_api_requester import GitApiRequester
from flask_restful import reqparse
from resources.base_resource import BaseResource
from common import error_code, status_code
from common.util import is_iter_empty
from models.repository import Repository


class GitRepositoryResource(BaseResource):
    def __init__(self):
        super().__init__()

    def get(self, pid=None, name=None):
        return self.__repository_information(pid, name)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('pid', required=True, help='pid is required')
        parser.add_argument("name", required=True, help="token is required")
        parser.add_argument("token", required=True, help="rp_name is required")
        args = parser.parse_args()

        # domain
        requester = GitApiRequester(args["token"])
        rp = requester.get_rp_by_name(args['name'])
        info = rp.get_info()
        repositories = self.db.collection(u'repositories').document().get({'pid': args['pid'],
                                                                           'name': args['name']})
        if self.__is_empty(repositories):
            return status_code.BAD_REQUEST
        else:
            repository = Repository(args['pid'], args['name'], info['commits'],
                                info['issues'], info['code_freq'], args['token'])
            self.db.collection('repositories').document().set(repository.to_dict())

            return status_code.OK

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('pid', required=True, help='pid is required')
        parser.add_argument("name", required=True, help="token is required")
        args = parser.parse_args()
        self.db.collection(u'repositories').document().delete({'pid': args['pid'],
                                                                'name': args['name']})
        return status_code.OK

    def __repository_information(self, pid, name):
        if pid is None and name is None:
            repositories = self.db.collection(u'repositories')
            if self.__is_empty(repositories):
                return error_code.NO_SUCH_ELEMENT
            return {'repositories': repository.to_dict() for repository in repositories}
        elif pid is not None and name is None:
            repositories = self.db.collection(u'repositories').where(u'pid', '==', pid)
            if self.__is_empty(repositories):
                return error_code.NO_SUCH_ELEMENT
            return {'repositories': repository.to_dict() for repository in repositories}
        elif pid is None and name is not None:
            repositories = self.db.collection(u'repositories').where(u'name', '==', name)
            if self.__is_empty(repositories):
                return error_code.NO_SUCH_ELEMENT
            return {'repositories': repository.to_dict() for repository in repositories}
        else:
            repositories = self.db.collection(u'repositories').document().get({'pid': pid,
                                                                               'name': name})
            if self.__is_empty(repositories):
                return error_code.NO_SUCH_ELEMENT
            else:
                return {'repository': repository.to_dict() for repository in repositories}

    def __is_empty(self, documents):
        return True if len(documents) > 0 else False
