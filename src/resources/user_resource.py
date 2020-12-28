from flask_restful import Resource, reqparse
from models.user_model import UserModel


class UserResource(Resource):
    def __init__(self):
        self._model = UserModel()

    def get(self):
        data, code = self._model.get_user_info_by_uid()
        return data, code

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True, help='name is required')
        parser.add_argument('email', required=True, help='email is required')
        args = parser.parse_args()
        # print(args['name'], args['email'])
        msg, code = self._model.add_user(args['name'], args['email'])
        return {
            'message': msg
        }, code

    def patch(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name')
        parser.add_argument('email')
        args = parser.parse_args()
        return self._model.update_user_info(email=args['email'], name=args['name'])
