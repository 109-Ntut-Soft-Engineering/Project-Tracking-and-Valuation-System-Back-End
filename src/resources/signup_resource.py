from flask import jsonify, abort
from flask_restful import Resource, reqparse
from entities.repo import Repo
from common import status_code, error_code
from common.status_code import is_client_error
from common.util import is_iter_empty
from models.user_model import UserModel
from utilities.github_api_requester import GithubApiRequester
from models.project_model import ProjectModel
import requests
import json
from common.constant import APIKEY


class SignUpResource(Resource):
    def __init__(self):
        self._apiKey = 'AIzaSyBSx_sJAvz0AmmffTDwODGAioXfyqP4Foc'

    def __signUp(self, email, password):
        firebaseSignUpAPI = 'https://identitytoolkit.googleapis.com/v1/accounts:signUp?key='+APIKEY
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
                firebaseSignUpAPI, data=parameters, headers=header)

            resp = json.loads(r.text)

            if 'error' not in resp:
                # print('66', json.dumps(resp))
                return {'idToken': resp['idToken'], 'refreshToken': resp['refreshToken']}
            else:
                error = resp['error']['message']
                if error == "EMAIL_EXISTS":
                    error = "此EMail已存在"
                elif "TOO_MANY_ATTEMPTS_TRY_LATER" in error:
                    error = "請稍後再試"

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
        return self.__signUp(args['email'], args['password'])
