import sys
import os.path

import pytest
from src.entities.user import User

class TestUser():
    @classmethod
    def setup_class(self):
        self.user = User(name='name', 
                            email='abc@gmail.com')
                        
    def test_constructor(self):
        assert self.user.name == 'name'
        assert self.user.email == 'abc@gmail.com'

    def test_from_dict(self):
        source = {
            'name' : 'name', 
            'email' : 'abc@gmail.com'
        }
        user = User.from_dict(source)
        assert user.name == 'name'
        assert user.email == 'abc@gmail.com'

    def test_to_dict(self):
        dest = self.user.to_dict()
        expect = {
            'name' : 'name', 
            'email' : 'abc@gmail.com'
        }
        assert dest == expect