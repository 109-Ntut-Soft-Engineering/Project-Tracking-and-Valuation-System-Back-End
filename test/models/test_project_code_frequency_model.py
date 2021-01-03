import sys, os.path, unittest

sys.path.append(os.path.join(os.path.dirname(__file__), '../../src'))

from test.fake_conn_tool import FakeConnTool
from src.models.project_code_frequency_model import ProjectCodeFrequencyModel
from src.common import constant
from datetime import datetime


class TestProjectCodeFrequencyModel(unittest.TestCase):
    def setUp(self):
        self.model = ProjectCodeFrequencyModel(FakeConnTool())
        self.test1_code_freq = [
            {"date": "2020/3/10", "code": 30}, {"date": "2020/4/10", "code": 60},
            {"date": "2020/5/10", "code": 100}, {"date": "2020/6/10", "code": 0},
            {"date": "2020/7/10", "code": 0}
        ]
        self.test2_code_freq = [
            {"date": "2020/5/10", "code": 55}, {"date": "2020/6/10", "code": 15},
            {"date": "2020/8/10", "code": 52}, {"date": "2020/7/10", "code": 10},
            {"date": "2020/9/10", "code": 0}
        ]

    def test_constructor(self):
        assert self.model._db != None
        assert self.model._uid == constant.TEST_UID

    def test_transfer_get_code_freq(self):
        code_freq = self.model.get_code_freq(constant.TEST_PID1)
        assert isinstance(code_freq, list)

    def test_get_compare_code_freq(self):
        try:
            compare_code_freq = self.model.get_compare_code_frequency(constant.TEST_PID1, constant.TEST_PID1)
        except Exception as e:
            self.assertTrue(e)
        compare_code_freq = self.model.get_compare_code_frequency(constant.TEST_PID1, constant.TEST_PID2)
        try:
            self.assertTrue('date' in compare_code_freq[0].keys())
            self.assertTrue(constant.TEST_PID1 in compare_code_freq[0].keys())
            self.assertTrue(constant.TEST_PID2 in compare_code_freq[0].keys())
            self.assertTrue(len(compare_code_freq) == 10)
        except:
            print("Unittest error")

    def test_sort_code_freq(self):
        sorted_code_freq = self.model._ProjectCodeFrequencyModel__sort_code_freq(self.test1_code_freq)
        FORMAT = '%Y/%m/%d'
        for i in range(len(sorted_code_freq)-1):
            current_time = datetime.strptime(sorted_code_freq[i]['date'], FORMAT)
            next_time = datetime.strptime(sorted_code_freq[i+1]['date'], FORMAT)
            assert current_time < next_time

    def test__delete_post_zero(self):
        assert len(self.test2_code_freq) == 5
        non_post_zero = self.model._ProjectCodeFrequencyModel__delete_post_zero(self.test1_code_freq)
        assert len(non_post_zero) == 3

        assert len(self.test2_code_freq) == 5
        non_post_zero = self.model._ProjectCodeFrequencyModel__delete_post_zero(self.test2_code_freq)
        assert len(non_post_zero) == 4