import sys, os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '../../src'))

from test.api.base_setting import BaseSetting
from src.config import BASE
from common import constant
import json

class TestWeekCommitApi(BaseSetting):
    def setUp(self) -> None:
        self.set_auth()
        self.test_pid1 = constant.TEST_PID1
        self.test_pid2 = constant.TEST_PID2

    def __get_week_commit(self, pid):
        return BASE + 'project/{}/week_commit'.format(pid)

    # Test single weekcommit
    def test_week_commit_api(self):
        # query without auth
        api = self.__get_week_commit(self.test_pid1)
        res = self.client.get(api)
        self.assert_401(res)

        # query exist pid code frequency (normal situation)
        res = self.client.get(api, headers=self.header)
        self.assert_200(res)

        # query not exist pid code frequency
        not_exsit_pid1 = 'tsakna2lknc'
        api = self.__get_week_commit(not_exsit_pid1)
        res = self.client.get(api, headers=self.header)
        data = json.loads(res.data.decode())
        self.assert_200(res)
        self.assertTrue(data['WeekCommit'] == {})
        
    def get_compare_week_commit(self, pid1, pid2):
        return BASE + 'project/compare/{}/{}/week_commit'.format(pid1, pid2)

    # Test multi weekcommit
    def test_compare_week_commit_api(self):
        # query without auth
        api = self.get_compare_week_commit(self.test_pid1, self.test_pid2)
        res = self.client.get(api)
        self.assert_401(res)

        # query exist pid code frequency (normal situation)
        res = self.client.get(api, headers=self.header)
        self.assert_200(res)

        # query not exist pid code frequency
        not_exsit_pid1 = 'tsakna2lknc'
        not_exsit_pid2 = 'sieatoa12feae'
        api = self.get_compare_week_commit(not_exsit_pid1, not_exsit_pid2)
        res = self.client.get(api, headers=self.header)
        data = json.loads(res.data.decode())
        self.assert_200(res)
        self.assertTrue(data['week_commit'] == {})