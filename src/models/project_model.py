from models.base_model import BaseModel
from entities.project import Project
from common import status_code, error_code
from common.status_code import is_client_error
from common.util import is_iter_empty
import sys

class ProjectModel(BaseModel):
    def get_project_information(self, name=None):
        if name is None:
            projects = self.db.collection(u'projects').where(u'owner', u'array_contains', self.uid).stream()
            return { 'projects': [project.to_dict() for project in projects]}
        else:
            projects = self.db.collection(u'projects').where(u'name', u'==', name).stream()
            if projects is None:
                return status_code.NOT_FOUND
            return { 'project': project.to_dict() for project in projects }

    def add_project(self, name, owner):
        if self.__is_project_name_exist(name):
            return status_code.BAD_REQUEST

        pid = self.__next_project_id()
        project = Project(pid=pid, name=name, owner=list(owner))

        self.db.collection(u'projects').document().set(project.to_dict())

        return status_code.OK

    def __is_project_name_exist(self, name):
        projects = self.db.collection(u'projects').where(u'name', u'==', name).stream()
        return not is_iter_empty(projects)[0]

    def __next_project_id(self):
        projects = self.db.collection(u'projects').stream()
        if projects is None:
            return 1
        *lst, last = projects
        last_project = last.to_dict()
        return int(last.to_dict()['pid']) + 1

    def delete_project(self, name):
        if not self.__is_project_name_exist(name):
            return status_code.NOT_FOUND

        projects = self.db.collection(u'projects').where(u'name', u'==', name).stream()
        for project in projects:
            project.reference.delete()
        return status_code.OK

    def update_project(self, name, owner, repositories):
        if not self.__is_project_name_exist(name):
            return status_code.NOT_FOUND

        project = self.__get_unique(self.db.collection(u'projects').where(u'name', u'==', name))
        project_dict = self.__init_project(project)

        update_data = {}
        code = self.__set_update_data(project_dict, owner, update_data, 'owner')
        if is_client_error(code):
            return code
        code = self.__set_update_data(project_dict, repositories, update_data, 'repositories')
        if is_client_error(code):
            return code

        if len(update_data) == 0:
            return status_code.BAD_REQUEST

        project.reference.set(update_data, merge=True)
        return status_code.OK

    def __init_project(self, project):
        project_dict = project.to_dict()
        if project_dict['owner'] is None:
            project_dict['owner'] = []
        if project_dict['repositories'] is None:
            project_dict['repositories'] = []
        return project_dict

    def __set_update_data(self, origin, update, update_data, field_name):
        code = self.__validate_update_array(origin, update, field_name)
        if code == status_code.OK:
            update_data[field_name] = list(set(update) | set(origin[field_name]))
        elif is_client_error(code):
            return code
        return status_code.OK

    def __validate_update_array(self, origin, update, field_name):
        if update is None:
            return error_code.NO_SUCH_ELEMENT
        if len(set(origin) & set(update)) == 0:
            return status_code.OK
        else:
            return status_code.BAD_REQUEST

    def __get_unique(self, collection):
        return next(collection.stream())