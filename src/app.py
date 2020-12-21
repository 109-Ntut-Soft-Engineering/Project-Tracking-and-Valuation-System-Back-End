from flask import Flask
from flask_restful import Api
from flask_cors import CORS
import config
from resources.user_resource import UserResource
from resources.projects_resource import ProjectsResource
from resources.project_resource import ProjectResource
from resources.project_code_frequency_resource import ProjectCodeFrequencyResource
from resources.repository_resource import RepositoryResource
from resources.authorization_resource import AuthResource
from resources.project_commit_resource import ProjectCommitResource
from resources.project_weekcommit_resource import ProjectWeekCommitResource
from resources.project_Issue_message_resource import ProjectIssueMessageResource
app = Flask("soft engineering")
app.config.from_object(config)
api = Api(app)
CORS(app)


api.add_resource(UserResource, '/user')
api.add_resource(ProjectsResource, '/project')
api.add_resource(ProjectResource, '/project/<string:name>')
api.add_resource(ProjectCommitResource, '/project/<string:name>/commit')
api.add_resource(AuthResource, '/auth', endpoint='auth')

api.add_resource(RepositoryResource, '/repository', endpoint='repositories')
api.add_resource(RepositoryResource,
                 '/repository/<string:name>', endpoint='repository')

# for code frequency
api.add_resource(ProjectCodeFrequencyResource, '/project/code_freq/<string:name>')

# for commit contribution
api.add_resource(ProjectWeekCommitResource, '/project/week_commit/<string:name>')

# for issue message
api.add_resource(ProjectIssueMessageResource, '/project/issue/<string:name>')


if __name__ == "__main__":  
    app.run()
