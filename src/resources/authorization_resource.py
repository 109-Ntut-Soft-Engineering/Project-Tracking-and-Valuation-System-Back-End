from flask import jsonify, abort
from flask_restful import Resource, reqparse
from common import error_code, status_code
from common.util import is_iter_empty
from common.status_code import is_client_error
from models.user_model import UserModel


class AuthResource(Resource):
    def __init__(self):
        self._model = UserModel('test_token')

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('code', required=True, help='code is required')
        args = parser.parse_args()
        msg, code = self._model.set_user_token(args['code'])
        print(msg, code)
        return {
            'message': msg
        }, code
