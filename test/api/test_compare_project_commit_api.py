import sys
import os.path

sys.path.append(os.path.join(os.path.dirname(__file__), '../../src'))

from test.api.base_setting import BaseSetting
from src.config import BASE
from common import constant


class TestCompareCommitApi(BaseSetting):
    def setUp(self) -> None:
        self.set_auth()
        self.test_pid1 = constant.TEST_PID1
        self.test_pid2 = constant.TEST_PID2

    def get_compare_commit_api(self, pid1, pid2):
        return BASE + 'project/compare/{}/{}/code_freq'.format(pid1, pid2)

    def test_compare_commit_api(self):
        # query without auth
        api = self.get_compare_commit_api(self.test_pid1, self.test_pid2)
        res = self.client.get(api)
        self.assert_401(res)

        # query exist pid code frequency (normal situation)
        api = self.get_compare_commit_api(self.test_pid1, self.test_pid2)
        res = self.client.get(api, headers=self.header)
        self.assert_200(res)
