import sys
import os.path

import pytest
from src.entities.commit import Commit
from src.entities.commits import Commits

class TestCommit():
    @classmethod
    def setup_class(self):
        self.commit1 = Commit(author='author1', 
                        message='message1', 
                        lines='100', 
                        time='2020/01/01')
        self.commit2 = Commit(author='author2', 
                        message='message2', 
                        lines='200', 
                        time='2020/01/02')
        self.commits = Commits('name', ['m1', 'm2', 'm3'], [self.commit1, self.commit2])

    def test_constructor(self):
        assert self.commits.name == 'name'
        assert self.commits.member == ['m1', 'm2', 'm3']
        assert self.commits.commit_list == [self.commit1, self.commit2]

    def test_from_dict(self):
        source = {
            'name' : 'name', 
            'member' : ['m1', 'm2', 'm3'], 
            'commit_list' : [self.commit1, self.commit2]
        }
        commits = Commits.from_dict(source)
        assert commits.name == 'name'
        assert commits.member == ['m1', 'm2', 'm3']
        assert commits.commit_list == [self.commit1, self.commit2]

    def test_to_dict(self):
        dest = self.commits.to_dict()
        expect = {
            'name' : 'name', 
            'member' : ['m1', 'm2', 'm3'], 
            'commit_list' : [
                {
                    'author' : 'author1', 
                    'message' : 'message1', 
                    'lines' : '100', 
                    'time' : '2020/01/01'
                }, 
                {
                    'author' : 'author2', 
                    'message' : 'message2', 
                    'lines' : '200', 
                    'time' : '2020/01/02'
                }]
        }
        assert dest == expect
    