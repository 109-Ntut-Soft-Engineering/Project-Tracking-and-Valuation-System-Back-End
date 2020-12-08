from models.base_model import BaseModel
from entities.user import User
from common import status_code, error_code
from common.status_code import is_client_error
from common.util import is_iter_empty
import requests
import json


class UserModel(BaseModel):
    def get_user_information(self, uid=None):
        if uid is None:
            users = self.db.collection(u'users').stream()
            return {'users': user.to_dict() for user in users}
        else:
            users = self.db.collection(u'users').where(
                u'uid', u'==', uid).stream()
            is_empty, users = is_iter_empty(users)
            if is_empty:
                return error_code.NO_SUCH_ELEMENT
            users = self.db.collection(u'users').where(
                u'uid', u'==', uid).stream()
            return {'user': user.to_dict() for user in users}

    def add_user(self, name, email):
        if self.__is_uid_exist(self.uid) or self.__is_email_exist(self.uid):
            return '發生錯誤', status_code.BAD_REQUEST

        user = User(name=name, email=email)

        self.db.collection(u'users').document(self.uid).set(user.to_dict())

        return '新增uid成功', status_code.OK

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
        users = self.db.collection(u'users').where(
            u'uid', u'==', self.uid).stream()
        return not is_iter_empty(users)[0]

    def __is_email_exist(self, email):
        users = self.db.collection(u'users').where(
            u'email', u'==', email).stream()
        return not is_iter_empty(users)[0]
