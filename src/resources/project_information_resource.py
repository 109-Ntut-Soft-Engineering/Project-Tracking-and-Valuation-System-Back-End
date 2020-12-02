from flask_restful import Resource, reqparse
from models.project_information_calculator import ProjectInformationCalculator
from models.project import Project
from resources.base_resource import BaseResource
from common import status_code
class ProjectCodeFrequencyResource(BaseResource):
    def __init__(self):
        super().__init__()
        self.test_token = 'ef4164107b7e4e2505abd8fced70951f44e51964'

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True, help="project's name is required")
        args = parser.parse_args()

        projects = self.db.collection(u'projects').where(u'name', u'==', args.name).get()

        if len(projects) == 0:
            return status_code.NOT_FOUND
        print('project:',  projects[0].to_dict())
        project = projects[0].to_dict()
        project = Project(project['pid'], project['name'], project['owner'], project['repositories'])
        calculator = ProjectInformationCalculator(project, self.test_token)
        return {"code_freq": calculator.get_code_freq()}, status_code.OK



class ProjectCommitsResource(Resource):
    def __init__(self):
        super().__init__()

    def post(self):
        pass

class ProjectIssuesResource(Resource):
    def __init__(self):
        super().__init__()

    def post(self):
        pass