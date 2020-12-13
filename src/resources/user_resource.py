from flask import jsonify, abort
from flask_restful import Resource, reqparse
from models.user_model import UserModel
from common import error_code, status_code
from common.util import is_iter_empty
from common.status_code import is_client_error


class UserResource(Resource):
    def __init__(self):
        self._model = UserModel()

    def get(self):
        data = self._model.get_user_information()
        if data == error_code.NO_SUCH_ELEMENT:
            abort(404)
        return jsonify(data)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True, help='name is required')
        parser.add_argument('email', required=True, help='email is required')
        args = parser.parse_args()
        print(args['name'], args['email'])
        msg, code = self._model.add_user(args['name'], args['email'])
        # if is_client_error(code):
        #     abort(code)
        return {
            'message': msg
        }, code
