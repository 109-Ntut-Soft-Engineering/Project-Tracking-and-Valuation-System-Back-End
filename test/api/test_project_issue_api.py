import sys, os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '../../src'))

from test.api.base_setting import BaseSetting
from src.config import BASE
from common import constant
import json

class TestIssueMessageApi(BaseSetting):
    def setUp(self) -> None:
        self.set_auth()
        self.test_pid1 = constant.TEST_PID1
        self.test_pid2 = constant.TEST_PID2

    def __get_issue(self, pid):
        return BASE + 'project/{}/issue'.format(pid)

    # Test single weekcommit
    def test_week_commit_api(self):
        # query without auth
        api = self.__get_issue(self.test_pid1)
        res = self.client.get(api)
        self.assert_401(res)

        # query exist pid code frequency (normal situation)
        res = self.client.get(api, headers=self.header)
        self.assert_200(res)

        # query not exist pid code frequency
        not_exsit_pid1 = 'tsakna2lknc'
        api = self.__get_issue(not_exsit_pid1)
        res = self.client.get(api, headers=self.header)
        data = json.loads(res.data.decode())
        self.assert_200(res)
        self.assertTrue(data['issues'] == {})