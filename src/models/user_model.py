from conn_tool import ConnTool
from entities.user import User
from common import status_code, error_code
from common.status_code import is_client_error
from common.util import is_iter_empty
import requests
import json


class UserModel():
    def __init__(self, id_token):
        _conn_tool = ConnTool(id_token)
        self._db = _conn_tool.db
        self._uid = _conn_tool.uid

    def get_user_information(self):
        users = self._db.collection(u'users').where(
            u'uid', u'==', self._uid).stream()
        is_empty, users = is_iter_empty(users)
        if is_empty:
            return error_code.NO_SUCH_ELEMENT
        users = self._db.collection(u'users').where(
            u'uid', u'==', self._uid).stream()
        return {'user': user.to_dict() for user in users}

    def add_user(self, name, email):
        if self.__is_uid_exist(self._uid) or self.__is_email_exist(self._uid):
            return status_code.BAD_REQUEST

        user = User(uid=self._uid, name=name, email=email)

        self._db.collection(u'users').document().set(user.to_dict())

        return status_code.OK

    def set_user_token(self, code):
        parameters = {
            'client_id': '4fc83f8cb4d05b3684de',
            'client_secret': 'f9f2503c8228d7d305e00fbcd01a52bfb59a387b',
            'code': code
        }
        header = {
            "Accept": "application/json"
        }
        r = requests.post(
            'https://github.com/login/oauth/access_token', data=parameters, headers=header)

        resp = json.loads(r.text)

        if "access_token" in resp:
            print(resp["access_token"])
            return 'Get access token success !', status_code.OK
        else:
            return resp["error_description"], status_code.BAD_REQUEST

    def __is_uid_exist(self, uid):
        users = self._db.collection(u'users').where(
            u'uid', u'==', self._uid).stream()
        return not is_iter_empty(users)[0]

    def __is_email_exist(self, email):
        users = self._db.collection(u'users').where(
            u'email', u'==', email).stream()
        return not is_iter_empty(users)[0]
