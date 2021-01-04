import sys, os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '../../src'))

import pytest
from src.common import constant
from test.fake_conn_tool import FakeConnTool
from src.models.project_issue_message_model import ProjectIssueMessageModel

class TestIssueMessageModel():
    @classmethod
    def setup_class(self):
        self.model = ProjectIssueMessageModel(FakeConnTool())

    def test_constructor(self):
        assert self.model._db != None
        assert self.model._uid == constant.TEST_UID

    def test_get_issues_fit_expectation(self):
        res = self.model.get_issues(constant.TEST_PID1)
        expect = [
            {
                'issue' : [],
                'name' : 'se-test'
            }
        ]
        assert res == expect

    def test_get_issues_from_not_exist_pid(self):
        res = self.model.get_issues(constant.TEST_PID2)
        assert res == {}