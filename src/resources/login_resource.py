from flask import jsonify, abort
from flask_restful import Resource, reqparse
from common import status_code, error_code
from common.status_code import is_client_error
from common.util import is_iter_empty
from models.user_model import UserModel
from utilities.github_api_requester import GithubApiRequester
from models.project_model import ProjectModel
import requests
import json
from common.constant import APIKEY


class LoginResource(Resource):

    def __login(self, email, password):
        firebaseSingInAPI = 'https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key='+APIKEY
        header = {
            "Accept": "application/json"
        }
        parameters = {
            'email': email,
            'password': password,
            'returnSecureToken': True
        }
        try:
            r = requests.post(
                firebaseSingInAPI, data=parameters, headers=header)

            resp = json.loads(r.text)
            print('77', json.dumps(resp))
            if 'error' not in resp:
                # print('66', json.dumps(resp))
                return {'idToken': resp['idToken'], 'refreshToken': resp['refreshToken']}
            else:
                error = resp['error']['message']
                if error == "INVALID_PASSWORD":
                    error = "密碼錯誤"
                elif "TOO_MANY_ATTEMPTS_TRY_LATER" in error:
                    error = "請稍後再試"
                elif error == "EMAIL_NOT_FOUND":
                    error = "此帳號不存在"

                return {'error': error}, status_code.BAD_REQUEST,
        except Exception as e:
            print(e)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', required=True, help='email is required.')
        parser.add_argument('password', required=True,
                            help='password is required.')
        args = parser.parse_args()
        # print(args)
        return self.__login(args['email'], args['password'])
