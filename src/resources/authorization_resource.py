from flask import jsonify, abort
from flask_restful import Resource, reqparse
from resources.base_resource import BaseResource
from common import error_code, status_code
from common.util import is_iter_empty
from common.status_code import is_client_error
from models.user_model import UserModel
from flask import request


class AuthResource(BaseResource):
    # method_decorators = [authenticate]

    def __init__(self):
        super().__init__()
        self._model = UserModel(self.db, self.uid)

    def post(self):

        # print(self._Idtoken)
        parser = reqparse.RequestParser()
        parser.add_argument('code', required=True, help='code is required')
        args = parser.parse_args()
        msg, code = self._model.set_user_token(args['code'])
        print(msg, code)
        return {
            'message': msg
        }, code
