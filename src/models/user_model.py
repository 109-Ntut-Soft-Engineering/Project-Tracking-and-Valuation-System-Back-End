from conn_tool import ConnTool
from entities.user import User
from common import status_code, error_code

import requests
import json
import sys
from conn_tool import ConnTool
from firebase_admin import auth
import firebase_admin


class UserModel():
    def __init__(self):
        _conn_tool = ConnTool()
        self._db = _conn_tool.db
        self._uid = _conn_tool.uid

    def get_user_info_by_email(self, email):

        try:
            uid = auth.get_user_by_email(email).uid
            user = self._db.collection('users').document(uid).get()
        except:
            return {'msg': '找不到使用者！'}, status_code.NOT_FOUND

        if user.exists:
            user_dict = User.from_dict(user.to_dict()).to_dict()
            user_dict.update({'uid': user.id})
            print(user_dict, file=sys.stderr)
            return user_dict, status_code.OK

    def get_user_info_by_uid(self, uid=None):
        if uid == None:
            user = self._db.collection('users').document(self._uid).get()
        else:
            try:
                auth.get_user(uid)
                user = self._db.collection('users').document(uid).get()
            except:
                return {'msg': '找不到使用者！'}, status_code.NOT_FOUND
        if user.exists:
            user_dict = User.from_dict(user.to_dict()).to_dict()
            user_dict.update({'uid': user.id})
            print(user_dict, file=sys.stderr)
            return user_dict, status_code.OK

    def get_user_githubToken(self, uid=None):
        info = None
        if uid == None:
            info = self._db.collection('users').document(
                self._uid).get().to_dict()
        else:
            info = self._db.collection('users').document(uid).get().to_dict()
        if 'Github' in info:
            return info['Github']
        else:
            return None

    def add_user(self, name, email):
        user = User(name=name, email=email)
        self._db.collection(u'users').document(self._uid).set(user.to_dict())
        return None, status_code.OK

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
            user = self._db.collection('users').document(self._uid)
            user.update({'Github': resp["access_token"]})
            return 'Get access token success !', status_code.OK
        else:
            return resp["error_description"], status_code.BAD_REQUEST

    def update_user_info(self, email, name):
        user = self._db.collection('users').document(self._uid)
        if user.get().exists:

            try:

                auth.update_user(self._uid, email=email)
                user.update({'name': name, 'email': email})
            except Exception as e:
                # print(type(e))
                if type(e) is firebase_admin._auth_utils.EmailAlreadyExistsError:
                    return {'error': 'Email已存在'}, status_code.BAD_REQUEST
                else:
                    return {'error': '未知錯誤'}, status_code.BAD_REQUEST

            return status_code.OK
