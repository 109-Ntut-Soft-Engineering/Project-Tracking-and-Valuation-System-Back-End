from models.project_code_frequency_model import ProjectCodeFrequencyModel
from entities.project import Project
from resources.base_resource import BaseResource
from common import status_code


class ProjectCodeFrequencyResource(BaseResource):
    def __init__(self):
        super().__init__()
        self.test_token = 'ef4164107b7e4e2505abd8fced70951f44e51964'

    def get(self, name):
        print('name', name)
        model = ProjectCodeFrequencyModel(self.db, self.uid)
        return {"code_freq": model.get_code_freq(name, self.test_token)}, status_code.OK
