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
            user = self.db.collection('users').document(uid)
            return user.to_dict()

    def get_user_githubToken(self):
        info = self.db.collection('users').document(self.uid).get().to_dict()
        if 'Github' in info:
            return info['Github']
        else:
            return None

    def add_user(self, name, email):

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
            # print(resp["access_token"])
            user = self.db.collection('users').document(self.uid)
            user.update({'Github': resp["access_token"]})
            return 'Get access token success !', status_code.OK
        else:
            return resp["error_description"], status_code.BAD_REQUEST
