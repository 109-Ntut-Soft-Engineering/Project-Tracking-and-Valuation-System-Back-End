from flask import jsonify, abort
from flask_restful import Resource, reqparse
from resources.base_resource import BaseResource
from models.user import User
from common import error_code, status_code
from common.util import is_iter_empty
from common.status_code import is_client_error

class UserResource(BaseResource):
    def get(self):
        data = self.__user_information(self.uid)
        if data == error_code.NO_SUCH_ELEMENT:
            abort(404)
        return jsonify(data)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True, help='name is required.')
        parser.add_argument('email', required=True, help='email is required')
        args = parser.parse_args()

        code = self.__add_user(args['name'], args['email'])
        if is_client_error(code):
            abort(code)
        return code
        
    def __user_information(self, uid=None):
        if uid is None:
            users = self.db.collection(u'users').stream()
            return { 'users': user.to_dict() for user in users }
        else:
            users = self.db.collection(u'users').where(u'uid', u'==', uid).stream()
            is_empty, users = is_iter_empty(users)
            if is_empty:
                return error_code.NO_SUCH_ELEMENT
            users = self.db.collection(u'users').where(u'uid', u'==', uid).stream()
            return { 'user': user.to_dict() for user in users }

    def __add_user(self, name, email):
        if self.__is_uid_exist(self.uid) or self.__is_email_exist(self.uid):
            return status_code.BAD_REQUEST

        user = User(uid=self.uid, name=name, email=email)

        self.db.collection(u'users').document().set(user.to_dict())

        return status_code.OK

    def __is_uid_exist(self, uid):
        users = self.db.collection(u'users').where(u'uid', u'==', self.uid).stream()
        return not is_iter_empty(users)[0]

    def __is_email_exist(self, email):
        users = self.db.collection(u'users').where(u'email', u'==', email).stream()
        return not is_iter_empty(users)[0]
