import sys
import os.path

import pytest
from src.entities.commit import Commit

class TestCommit():
    @classmethod
    def setup_class(self):
        self.commit = Commit(author='author', 
                        message='message', 
                        lines='100', 
                        time='2020/01/01')

    def test_constructor(self):
        assert self.commit.author == 'author'
        assert self.commit.message == 'message'
        assert self.commit.lines == '100'
        assert self.commit.time == '2020/01/01'

    def test_from_dict(self):
        source = {
            'author' : 'author', 
            'message' : 'message', 
            'lines' : '100', 
            'time' : '2020/01/01'
        }
        commit = Commit.from_dict(source)
        assert commit.author == 'author'
        assert commit.message == 'message'
        assert commit.lines == '100'
        assert commit.time == '2020/01/01'

    def test_to_dict(self):
        dest = self.commit.to_dict()
        expect = {
            'author' : 'author', 
            'message' : 'message', 
            'lines' : '100', 
            'time' : '2020/01/01'
        }
        assert dest == expect
    