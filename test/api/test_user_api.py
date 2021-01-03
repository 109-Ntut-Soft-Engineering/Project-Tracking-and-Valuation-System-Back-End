import sys
import os.path

sys.path.append(os.path.join(os.path.dirname(__file__), '../../src'))

from test.api.base_setting import BaseSetting
from src.config import BASE


class TestUserApi(BaseSetting):
    def setUp(self) -> None:
        self.set_auth()
        self.test_pid = 'Qb2783tRIxZeGKZYrVDh'

    def get_code_freq_api(self, pid):
        return BASE + 'project/{}/code_freq'.format(pid)

    def test_code_frequency_api(self):
        # query without auth
        api = self.get_code_freq_api(self.test_pid)
        res = self.client.get(api)
        self.assert_401(res)

        # query exist pid code frequency (normal situation)
        api = self.get_code_freq_api(self.test_pid)
        res = self.client.get(api, headers=self.header)
        self.assert_200(res)

        # query not exist pid code frequency
        not_exsit_pid = 'tsakna2lknc'
        api = self.get_code_freq_api(not_exsit_pid)
        res = self.client.get(api, headers=self.header)
        self.assert_404(res)
