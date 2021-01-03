import sys, os.path

sys.path.append(os.path.join(os.path.dirname(__file__), '../../src'))

import pytest
from test.fake_conn_tool import FakeConnTool
from src.models.project_model import ProjectModel
from src.common import constant
from src.common import status_code
from google.cloud import firestore

class TestProjectModel():
    @classmethod
    def setup_class(self):
        self.model = ProjectModel(FakeConnTool())

    @classmethod
    def get_project_by_pid(self, pid):
        pros, code = self.model.get_project_list()
        for pro in pros['projects']:
            if pro['id'] == pid:
                return pro
    
    @classmethod
    def get_pid_by_name(self, name):
        pros, code = self.model.get_project_list()
        pid = None
        for pro in pros['projects']:
            if pro['name'] == name:
                pid = pro['id']
                break
        return pid

    def test_constructor(self):
        assert self.model._db != None
        assert self.model._uid == constant.TEST_UID

    def test_get_project_list(self):
        res = self.model.get_project_list()
        expect = {
            'projects': [
                {
                    'name' : 'test_name3', 
                    'owner' : {
                        'name': 'abc', 
                        'email': 'abc@gmail.com', 
                        'uid': self.model._uid
                    }, 
                    'collaborator' : [], 
                    'repositories' : {
                        'Github' : [263537889]
                    }, 
                    'updated' : '2021-01-02 08:19:51.374000+00:00', 
                    'id': 'bv10AHp87ZtD93pPFfYh'
                }, 
                {
                    'name' : 'test_name2', 
                    'owner' : {
                        'name': 'abc', 
                        'email': 'abc@gmail.com', 
                        'uid': self.model._uid
                    }, 
                    'collaborator' : [], 
                    'repositories' : {
                        'Github' : [182191121]
                    }, 
                    'updated' : '2021-01-02 08:19:19.987000+00:00', 
                    'id': 'hNR8NR81T98kPec31ryP'
                }, 
                {
                    'name' : 'test_name', 
                    'owner' : {
                        'name': 'abc', 
                        'email': 'abc@gmail.com', 
                        'uid': self.model._uid
                    }, 
                    'collaborator' : [], 
                    'repositories' : {
                        'Github' : [324982851]
                    }, 
                    'updated' : '2021-01-02 08:13:59.648000+00:00', 
                    'id': constant.TEST_PID1
                }, 
                {
                    'name' : 'test_name_compare', 
                    'owner' : {
                        'name': 'abc', 
                        'email': 'abc@gmail.com', 
                        'uid': self.model._uid
                    }, 
                    'collaborator' : [], 
                    'repositories' : {
                        'Github' : [325248132]
                    }, 
                    'updated' : '2021-01-03 07:50:42.647000+00:00', 
                    'id': 'testing_id_compare'
                }
            ]
        }
        assert res == (expect, 200)

    def test_add_and_delete_project(self):
        self.model.add_project('test_add_project')
        pros, code = self.model.get_project_list()
        expect = None
        pid = None
        for pro in pros['projects']:
            if pro['name'] == 'test_add_project':
                expect = pro
                pid = pro['id']
        assert expect != None
        self.model.delete_project(self.get_pid_by_name('test_add_project'))

    def test_when_name_exist_then_add_project_should_400(self):
        self.model.add_project('test_add_repeat')
        pros, code = self.model.add_project('test_add_repeat')
        assert pros == None
        assert code == status_code.BAD_REQUEST
        self.model.delete_project(self.get_pid_by_name('test_add_repeat'))

    def test_is_project_name_used(self):
        assert self.model._ProjectModel__is_project_name_used('test_repeat_name') == False
        self.model.add_project('test_repeat_name')
        assert self.model._ProjectModel__is_project_name_used('test_repeat_name') == True
        self.model.delete_project(self.get_pid_by_name('test_repeat_name'))

    def test_delete_not_exist_project_should_404(self):
        data, code = self.model.delete_project('no_such_pid')
        assert data == None
        assert code == status_code.NOT_FOUND

    def test_is_project_owner(self):
        project1 = {
            'collaborator': [], 
            'name': 'test', 
            'owner': constant.TEST_UID, 
            'repositories': {
                'Github': [21212121]
            }, 
            'updated' : '2011-11-04 00:05:23.283000+00:00'
        }
        project2 = {
            'collaborator': [], 
            'name': 'test', 
            'owner': 'other_guy', 
            'repositories': {
                'Github': [21212121]
            }, 
            'updated' : '2011-11-04 00:05:23.283000+00:00'
        }
        assert self.model._ProjectModel__is_project_owner(project1, constant.TEST_UID) == True
        assert self.model._ProjectModel__is_project_owner(project2, constant.TEST_UID) == False

    def test_update_name(self):
        self.model.add_project('test_update_name')
        pros, code = self.model.get_project_list()
        pid = None
        for pro in pros['projects']:
            if pro['name'] == 'test_update_name':
                expect = pro
                pid = pro['id']
        data, code = self.model.update_name(pid, 'updated')
        update_pro = self.model._db.collection('projects').document(pid).get().to_dict()
        assert update_pro['name'] == 'updated'
        self.model.delete_project(self.get_pid_by_name('test_update_name'))
        self.model.delete_project(self.get_pid_by_name('updated'))

    def test_update_name_no_name_parameter(self):
        self.model.add_project('test_update_name_no_name')
        pros, code = self.model.get_project_list()
        pid = None
        for pro in pros['projects']:
            if pro['name'] == 'test_update_name_no_name':
                expect = pro
                pid = pro['id']
        data, code = self.model.update_name(pid, '')
        assert data == 'name is require'
        assert code == status_code.BAD_REQUEST
        self.model.delete_project(self.get_pid_by_name('test_update_name_no_name'))

    def test_update_name_no_such_pid(self):
        self.model.add_project('test_update_name_wrong_pid')
        data, code = self.model.update_name('wrong_pid', 'updated')
        assert data == None
        assert code == status_code.NOT_FOUND
        self.model.delete_project(self.get_pid_by_name('test_update_name_wrong_pid'))
