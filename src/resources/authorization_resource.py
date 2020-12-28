from flask_restful import Resource, reqparse
from models.user_model import UserModel
from conn_tool import ConnTool

class AuthResource(Resource):
    def __init__(self):
        self._model = UserModel(ConnTool())

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('code', required=True, help='code is required')
        args = parser.parse_args()
        msg, code = self._model.set_user_token(args['code'])
        print(msg, code)
        return {
            'message': msg
        }, code
