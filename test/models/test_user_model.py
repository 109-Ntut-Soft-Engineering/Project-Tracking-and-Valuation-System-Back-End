from test.fake_conn_tool import FakeConnTool
from src.models.user_model import UserModel
from src.entities.user import User
from src.common import constant
import datetime
import sys
import os.path
import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), '../../src'))


class TestUserModel():
    @classmethod
    def setup_class(self):
        self.model = UserModel(FakeConnTool())

    def test_get_user_info_by_email(self):
        email = 'abc@gmail.com'

        expect = {
            'name': 'name',
            'email': 'abc@gmail.com',
            'uid': 'KDD0wVZh0Rb6eLFb2KeWBgKMjiH2'
        }
        info = self.model.get_user_info_by_email(email)
        assert(info, expect)

    def test_get_user_info_by_uid(self):
        uid = 'KDD0wVZh0Rb6eLFb2KeWBgKMjiH2'

        expect = {
            'name': 'name',
            'email': 'abc@gmail.com',
            'uid': 'KDD0wVZh0Rb6eLFb2KeWBgKMjiH2'
        }
        info = self.model.get_user_info_by_uid(uid)
        assert(info, expect)
