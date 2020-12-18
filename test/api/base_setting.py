import requests
from src.app import app
from flask_testing import TestCase


class BaseSetting(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        return app

    def set_auth(self):
        self.test_account = {
            "email": 'wei.141227@gmail.com',
            'password': 'password',
            'returnSecureToken': True
        }
        self.id_token = self.get_id_token(self.test_account)
        self.header = {
            'Authorization': 'Bearer '+self.id_token,
            'Content-Type': 'application/x-www-form-urlencoded'
        }

    def get_id_token(self, data):
        api_key = 'AIzaSyBSx_sJAvz0AmmffTDwODGAioXfyqP4Foc'
        auth_api = 'https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key='+api_key
        res = requests.post(auth_api, data)
        if res.status_code == 200:
            print('idToken:', res.json()['idToken'])
            return res.json()['idToken']
        else:
            return None