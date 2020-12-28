import sys
import os.path

import pytest
import datetime
from src.entities.project import Project

class TestProject():
    @classmethod
    def setup_class(self):
        self.project = Project(name='name', 
                        owner='owner', 
                        collaborator=['c1', 'c2'], 
                        repositories={
                            'Github' : ['g1', 'g2']
                        }, 
                        updated=datetime.datetime(2011, 11, 4, 
                            0, 5, 23, 283000, 
                            tzinfo=datetime.timezone.utc)
                        )

    def test_constructor(self):
        assert self.project.name == 'name'
        assert self.project.owner == 'owner'
        assert self.project.collaborator == ['c1', 'c2']
        assert self.project.repositories == {
            'Github' : ['g1', 'g2']
        }
        assert self.project.updated == datetime.datetime(2011, 11, 4, 
            0, 5, 23, 283000, 
            tzinfo=datetime.timezone.utc
        )

    def test_from_dict(self):
        source = {
            'name' : 'name', 
            'owner' : 'owner', 
            'collaborator' : ['c1', 'c2'], 
            'repositories' : {
                'Github' : ['g1', 'g2']
            }, 
            'updated' : datetime.datetime(2011, 11, 4, 
                0, 5, 23, 283000, 
                tzinfo=datetime.timezone.utc
            )
        }
        project = Project.from_dict(source)
        assert project.name == 'name'
        assert project.owner == 'owner'
        assert project.collaborator == ['c1', 'c2']
        assert project.repositories == {
            'Github' : ['g1', 'g2']
        }
        assert project.updated == datetime.datetime(2011, 11, 4, 
            0, 5, 23, 283000, 
            tzinfo=datetime.timezone.utc
        )

    def test_to_dict(self):
        dest = self.project.to_dict()
        expect = {
            'name' : 'name', 
            'owner' : 'owner', 
            'collaborator' : ['c1', 'c2'], 
            'repositories' : {
                'Github' : ['g1', 'g2']
            }, 
            'updated' : '2011-11-04 00:05:23.283000+00:00'
        }
        assert dest == expect